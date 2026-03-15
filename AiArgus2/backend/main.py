from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import numpy as np
import cv2
import os
import subprocess
import imageio_ffmpeg
from typing import List
import json
import torch
from ultralytics.nn.tasks import DetectionModel
from torch.nn.modules.container import Sequential
import base64

# Store the original torch.load function
original_torch_load = torch.load

# Create a wrapper function that sets weights_only=False
def custom_torch_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)

# Replace torch.load with our custom version
torch.load = custom_torch_load

# ============================================================
# PRE-LOAD MODELS AT STARTUP (Optimization #1)
# Models are loaded once and reused for every request
# ============================================================
print("Loading YOLO models at startup...")
detection_model = YOLO('yolov8n.pt')
segmentation_model = YOLO('yolov8n-seg.pt')
print("All models loaded successfully!")

def reencode_video_h264(input_path: str, output_path: str):
    """Re-encode a video file to H.264 codec using ffmpeg for browser compatibility."""
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe,
        '-y',              # overwrite output
        '-i', input_path,  # input file
        '-c:v', 'libx264', # H.264 codec
        '-preset', 'fast',
        '-crf', '23',
        '-pix_fmt', 'yuv420p',  # max browser compatibility
        '-movflags', '+faststart',  # enable streaming
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def parse_color_hex(color: str):
    """Convert HEX color string to BGR tuple for OpenCV."""
    color_hex = color.lstrip('#')
    if len(color_hex) == 3:
        color_hex = ''.join([c*2 for c in color_hex])
    r = int(color_hex[0:2], 16)
    g = int(color_hex[2:4], 16)
    b = int(color_hex[4:6], 16)
    return (b, g, r)  # BGR for OpenCV

app = FastAPI()

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# COCO class names
names = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane',
        5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 
        10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 
        13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 
        18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 
        23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 
        27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 
        32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 
        36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 
        40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 
        45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 
        50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 
        55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 
        60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 
        65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 
        69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 
        74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 
        78: 'hair drier', 79: 'toothbrush'}

names_list = [name for name in names.values()]

def read_image_bytes(image_bytes, task):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

@app.get("/api/class-names")
async def get_class_names():
    return {"class_names": names_list}

@app.post("/api/detect")
async def detect_objects(
    file: UploadFile = File(...),
    task: str = Form("detection"),
    selected_classes: str = Form(None),
    threshold: float = Form(0.25),
    show_labels: bool = Form(True),
    show_confidence: bool = Form(True),
    color: str = Form("#B9282B"),
    thickness: int = Form(2)
):
    try:
        print(f"\n=== Starting {task} process ===")
        
        if selected_classes is None:
            selected_classes = names_list
        else:
            selected_classes = json.loads(selected_classes)

        content = await file.read()
        file_type = file.content_type.split('/')[0]
        print(f"Processing {file_type} file: {file.filename}, size: {len(content)} bytes")

        color_bgr = parse_color_hex(color)

        if file_type == "image":
            try:
                image = read_image_bytes(content, task)
                print(f"Image shape: {image.shape}")
                
                if task == "detection":
                    # Use pre-loaded detection model
                    result = detection_model.predict(image, verbose=True)
                    
                    image_with_boxes = image.copy()
                    boxes = result[0].boxes
                    
                    for i in range(len(boxes)):
                        box = boxes[i]
                        confidence = float(box.conf)
                        class_id = int(box.cls)
                        class_name = names[class_id]
                        
                        if class_name in selected_classes and confidence > threshold:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            cv2.rectangle(image_with_boxes, (x1, y1), (x2, y2), color_bgr, thickness)
                            
                            if show_confidence:
                                cv2.putText(image_with_boxes, 
                                    f"{confidence:.2f}",
                                    (x2 - 30, y1 + 12), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_bgr, 1)

                            if show_labels:
                                cv2.putText(image_with_boxes, 
                                    class_name, 
                                    (x1 + 6, y1 + 12), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_bgr, 1)

                    # Encode image
                    success, buffer = cv2.imencode('.png', image_with_boxes)
                    if not success:
                        raise Exception("Failed to encode image as PNG")
                    
                    image_base64 = base64.b64encode(buffer.tobytes()).decode('utf-8')
                    return {
                        "image": image_base64,
                        "format": "png",
                        "message": "Detection completed successfully"
                    }
                
                elif task == "segmentation":
                    # Use pre-loaded segmentation model
                    results = segmentation_model.predict(image, verbose=True)
                    
                    if not results or len(results) == 0:
                        return {"error": "No segmentation results found"}
                    
                    result = results[0]
                    
                    if not hasattr(result, 'masks') or result.masks is None:
                        return {"error": "No masks found in segmentation results"}
                    
                    output_image = image.copy()
                    overlay = output_image.copy()
                    np.random.seed(42)
                    class_color_map = {}

                    for i, (box, mask) in enumerate(zip(result.boxes, result.masks)):
                        try:
                            confidence = float(box.conf)
                            class_id = int(box.cls)
                            class_name = names[class_id]
                            if confidence < threshold or class_name not in selected_classes:
                                continue
                            if class_id not in class_color_map:
                                class_color_map[class_id] = tuple(np.random.randint(0, 255, 3).tolist())
                            seg_color = class_color_map[class_id]
                            mask_data = mask.data[0].cpu().numpy()
                            mask_resized = cv2.resize(mask_data, (image.shape[1], image.shape[0]))
                            mask_bin = (mask_resized > 0.5).astype(np.uint8)
                            colored_mask = np.zeros_like(output_image, dtype=np.uint8)
                            for c in range(3):
                                colored_mask[:,:,c] = seg_color[c]
                            alpha = 0.5
                            overlay[mask_bin == 1] = cv2.addWeighted(output_image, 1-alpha, colored_mask, alpha, 0)[mask_bin == 1]
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            label = f"{class_name} {confidence:.2f}"
                            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                            cv2.rectangle(overlay, (x1, y1 - th - 6), (x1 + tw, y1), seg_color, -1)
                            cv2.putText(overlay, label, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
                        except Exception as e:
                            print(f"Error processing detection {i}: {str(e)}")
                            continue
                    
                    output_image = overlay

                    _, buffer = cv2.imencode('.png', output_image)
                    image_base64 = base64.b64encode(buffer.tobytes()).decode('utf-8')
                    return {
                        "image": image_base64,
                        "format": "png",
                        "message": "Segmentation completed successfully"
                    }
            
            except Exception as e:
                print(f"Error processing image: {str(e)}")
                return {"error": str(e)}
        
        elif file_type == "video":
            # Save the uploaded video
            temp_file = "temp_video.mp4"
            with open(temp_file, "wb") as f:
                f.write(content)
            
            # Get video properties for the writer
            cap = cv2.VideoCapture(temp_file)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            output_file = "output.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
            
            # Przyspieszenie na CPU: inferencja co N klatek
            frame_skip = 2
            
            if task == "detection":
                print(f"TASK: OBJECT DETECTION (Video - {total_frames} frames, frame_skip={frame_skip})")
                
                frame_idx = 0
                last_boxes = None
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                        
                    frame_idx += 1
                    print(f"\rProcessing frame {frame_idx}/{total_frames}", end="", flush=True)
                    
                    # Run prediction only every 'frame_skip' frames
                    if frame_idx % frame_skip == 1 or last_boxes is None:
                        result = detection_model.predict(frame, verbose=False)[0]
                        last_boxes = result.boxes
                    
                    if last_boxes is not None:
                        for i in range(len(last_boxes.cls)):
                            class_name = names[int(last_boxes.cls[i])]
                            if class_name in selected_classes:
                                confidence = float(last_boxes.conf[i])
                                if confidence > threshold:
                                    x1, y1, x2, y2 = map(int, last_boxes.xyxy[i])
                                    
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), color_bgr, thickness)

                                    # Build label text
                                    label_parts = []
                                    if show_labels:
                                        label_parts.append(class_name)
                                    if show_confidence:
                                        label_parts.append(f"{confidence:.2f}")
                                    
                                    if label_parts:
                                        label = " ".join(label_parts)
                                        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                                        # Draw background rectangle for readability
                                        cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 4, y1), color_bgr, -1)
                                        cv2.putText(frame, label, (x1 + 2, y1 - 4),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
                    out.write(frame)
                print(f"\nDetection complete: {frame_idx} frames processed")
                
            elif task == "segmentation":
                print(f"TASK: SEGMENTATION (Video - {total_frames} frames, frame_skip={frame_skip})")
                
                np.random.seed(42)
                class_color_map = {}
                
                frame_idx = 0
                last_masks = None
                last_boxes = None
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                        
                    frame_idx += 1
                    print(f"\rProcessing frame {frame_idx}/{total_frames}", end="", flush=True)
                    overlay = frame.copy()
                    
                    # Run prediction only every 'frame_skip' frames
                    if frame_idx % frame_skip == 1 or last_boxes is None:
                        # Zmniejszenie rozdzielczości do 480p też pomaga na CPU
                        result = segmentation_model.predict(frame, imgsz=480, verbose=False)[0]
                        last_boxes = result.boxes
                        last_masks = result.masks
                    
                    masks = last_masks
                    boxes = last_boxes
                    
                    if masks is None or boxes is None:
                        out.write(frame)
                        continue
                    
                    for i in range(len(masks)):
                        if i < len(boxes):
                            confidence = float(boxes[i].conf)
                            class_id = int(boxes[i].cls)
                            class_name = names[class_id]
                            
                            if class_name in selected_classes and confidence > threshold:
                                if class_id not in class_color_map:
                                    class_color_map[class_id] = tuple(np.random.randint(60, 255, 3).tolist())
                                obj_color = class_color_map[class_id]
                                
                                mask_data = masks[i].data[0].cpu().numpy()
                                mask = cv2.resize(mask_data, (width, height))
                                mask_bin = (mask > 0.5).astype(np.uint8)
                                
                                colored_region = np.zeros_like(frame, dtype=np.uint8)
                                colored_region[:] = obj_color
                                overlay[mask_bin == 1] = cv2.addWeighted(
                                    frame, 0.5, colored_region, 0.5, 0
                                )[mask_bin == 1]
                                
                                mask_uint8 = (mask_bin * 255).astype(np.uint8)
                                contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                cv2.drawContours(overlay, contours, -1, obj_color, 3)
                                
                                if show_labels or show_confidence:
                                    x1, y1, x2, y2 = map(int, boxes[i].xyxy[0])
                                    label_parts = []
                                    if show_labels:
                                        label_parts.append(class_name)
                                    if show_confidence:
                                        label_parts.append(f"{confidence:.2f}")
                                    
                                    if label_parts:
                                        label = " ".join(label_parts)
                                        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                                        cv2.rectangle(overlay, (x1, y1 - th - 8), (x1 + tw + 4, y1), obj_color, -1)
                                        cv2.putText(overlay, label, (x1 + 2, y1 - 4),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    out.write(overlay)
                print(f"\nSegmentation complete: {frame_idx} frames processed")
            
            cap.release()
            out.release()
            
            # Re-encode to H.264 for browser compatibility
            h264_output = "output_h264.mp4"
            reencode_video_h264(output_file, h264_output)
            
            # ============================================================
            # BINARY STREAMING RESPONSE (Optimization #3)
            # Send video as binary stream instead of base64 in JSON
            # ============================================================
            def video_stream():
                with open(h264_output, "rb") as f:
                    while chunk := f.read(1024 * 1024):  # 1MB chunks
                        yield chunk
            
            return StreamingResponse(
                video_stream(),
                media_type="video/mp4",
                headers={"Content-Disposition": "inline; filename=output.mp4"}
            )
        
        return {"error": "Unsupported file type or task"}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)