from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import numpy as np
import cv2
import os
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

def hex_to_bgr(value):
    value = value.lstrip('#')
    lv = len(value)
    rgb_value = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    r_value, g_value, b_value = rgb_value
    bgr_value = (b_value, g_value, r_value)
    rgb_value = (r_value, g_value, b_value)
    return bgr_value, rgb_value

def read_image_bytes(image_bytes, task):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Zawsze używamy BGR
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
        print(f"Task type: {task}")
        
        if selected_classes is None:
            selected_classes = names_list
        else:
            selected_classes = json.loads(selected_classes)

        content = await file.read()
        file_type = file.content_type.split('/')[0]
        print(f"Processing {file_type} file: {file.filename}, size: {len(content)} bytes")

        if file_type == "image":
            try:
                image = read_image_bytes(content, task)
                print(f"Successfully read image with shape: {image.shape}")
                
                if task == "detection":
                    print("Loading YOLO model...")
                    try:
                        model = YOLO('yolov8n.pt')
                        print("Model loaded successfully")
                    except Exception as e:
                        print(f"Error loading model: {str(e)}")
                        return {"error": f"Failed to load YOLO model: {str(e)}"}
                    
                    print("Running detection...")
                    try:
                        result = model.predict(image, verbose=True)
                        print(f"Detection complete. Found {len(result[0].boxes.cls)} objects")
                    except Exception as e:
                        print(f"Error during prediction: {str(e)}")
                        return {"error": f"Failed to run detection: {str(e)}"}
                    
                    # Convert HEX to BGR properly
                    color_hex = color.lstrip('#')
                    if len(color_hex) == 3:
                        color_hex = ''.join([c*2 for c in color_hex])
                    color_bgr = tuple(int(color_hex[i:i+2], 16) for i in (4, 2, 0))  # RGB to BGR
                    print(f"Using color BGR: {color_bgr}")
                    
                    # Create a copy of the image for drawing
                    image_with_boxes = image.copy()
                    print(f"Original image shape: {image.shape}")
                    
                    # Debug YOLO results
                    print("\nYOLO Detection Results:")
                    print(f"Number of boxes: {len(result[0].boxes.cls)}")
                    
                    # Use YOLO results directly
                    boxes = result[0].boxes
                    print(f"Boxes type: {type(boxes)}")
                    print(f"Boxes attributes: {dir(boxes)}")
                    
                    for i in range(len(boxes)):
                        box = boxes[i]
                        confidence = float(box.conf)
                        class_id = int(box.cls)
                        class_name = names[class_id]
                        
                        print(f"\nObject {i+1}:")
                        print(f"Class: {class_name} (ID: {class_id})")
                        print(f"Confidence: {confidence}")
                        print(f"Box coordinates: {box.xyxy[0]}")
                        
                        if class_name in selected_classes and confidence > threshold:
                            # Get box coordinates in xyxy format
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            print(f"Drawing box at: ({x1}, {y1}) to ({x2}, {y2})")
                            
                            # Draw rectangle
                            cv2.rectangle(image_with_boxes, (x1, y1), (x2, y2), color_bgr, thickness)
                            
                            if show_confidence:
                                cv2.putText(image_with_boxes, 
                                    f"{confidence:.2f}",
                                    (x2 - 30, y1 + 12), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    0.5, 
                                    color_bgr, 
                                    1)

                            if show_labels:
                                cv2.putText(image_with_boxes, 
                                    class_name, 
                                    (x1 + 6, y1 + 12), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    0.5, 
                                    color_bgr, 
                                    1)

                    # Convert image to bytes
                    print("\nConverting image to bytes...")
                    try:
                        output_image_rgb = cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB)
                        _, buffer = cv2.imencode('.png', output_image_rgb)
                        image_bytes = buffer.tobytes()
                        print(f"Image converted to bytes, length: {len(image_bytes)}")
                    except Exception as e:
                        print(f"Error converting image: {str(e)}")
                        return {"error": f"Failed to convert image: {str(e)}"}
                    
                    print("=== Detection Process Completed ===")
                    return {
                        "image": image_bytes.hex(),
                        "format": "png",
                        "message": "Detection completed successfully"
                    }
                
                elif task == "segmentation":
                    print("Starting segmentation process...")
                    try:
                        # Load the model
                        print("Loading YOLO segmentation model...")
                        model = YOLO("yolov8n-seg.pt")
                        print("Model loaded successfully")
                        
                        # Run prediction
                        print("Running prediction...")
                        results = model.predict(image, verbose=True)
                        print(f"Prediction complete. Number of results: {len(results)}")
                        
                        if not results or len(results) == 0:
                            print("No results returned from model")
                            return {"error": "No segmentation results found"}
                        
                        # Get the first result
                        result = results[0]
                        print(f"Result type: {type(result)}")
                        print(f"Result attributes: {dir(result)}")
                        
                        # Check for masks
                        if not hasattr(result, 'masks') or result.masks is None:
                            print("No masks found in results")
                            return {"error": "No masks found in segmentation results"}
                        
                        print(f"Number of masks: {len(result.masks)}")
                        
                        # Create output image
                        output_image = image.copy()
                        
                        # Prepare overlay for alpha blending
                        overlay = output_image.copy()
                        np.random.seed(42)  # For reproducible colors per run
                        class_color_map = {}

                        for i, (box, mask) in enumerate(zip(result.boxes, result.masks)):
                            try:
                                confidence = float(box.conf)
                                class_id = int(box.cls)
                                class_name = names[class_id]
                                if confidence < threshold or class_name not in selected_classes:
                                    continue
                                # Generate or reuse color for this class
                                if class_id not in class_color_map:
                                    class_color_map[class_id] = tuple(np.random.randint(0, 255, 3).tolist())
                                color = class_color_map[class_id]
                                # Prepare mask
                                mask_data = mask.data[0].cpu().numpy()
                                mask_resized = cv2.resize(mask_data, (image.shape[1], image.shape[0]))
                                mask_bin = (mask_resized > 0.5).astype(np.uint8)
                                # Create colored mask
                                colored_mask = np.zeros_like(output_image, dtype=np.uint8)
                                for c in range(3):
                                    colored_mask[:,:,c] = color[c]
                                # Alpha blend mask
                                alpha = 0.5
                                overlay[mask_bin == 1] = cv2.addWeighted(output_image, 1-alpha, colored_mask, alpha, 0)[mask_bin == 1]
                                # Draw label on colored rectangle
                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                label = f"{class_name} {confidence:.2f}"
                                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                                cv2.rectangle(overlay, (x1, y1 - th - 6), (x1 + tw, y1), color, -1)
                                cv2.putText(overlay, label, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
                            except Exception as e:
                                print(f"Error processing detection {i}: {str(e)}")
                                import traceback
                                print(traceback.format_exc())
                                continue
                        
                        output_image = overlay

                        # Convert image to bytes
                        print("\nConverting image to bytes...")
                        try:
                            # Convert BGR to RGB
                            output_image_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
                            # Encode image to bytes
                            _, buffer = cv2.imencode('.png', output_image_rgb)
                            image_bytes = buffer.tobytes()
                            print(f"Image converted to bytes, length: {len(image_bytes)}")
                        except Exception as e:
                            print(f"Error converting image: {str(e)}")
                            return {"error": f"Failed to convert image: {str(e)}"}
                        
                        return {
                            "image": image_bytes.hex(),
                            "format": "png",
                            "message": "Segmentation completed successfully"
                        }
                        
                    except Exception as e:
                        print(f"Error during segmentation: {str(e)}")
                        import traceback
                        print(traceback.format_exc())
                        return {"error": f"Error during segmentation: {str(e)}"}
            
            except Exception as e:
                print(f"Error processing image: {str(e)}")
                return {"error": str(e)}
        
        elif file_type == "video":
            # Save the uploaded video
            temp_file = "temp_video.mp4"
            with open(temp_file, "wb") as f:
                f.write(content)
            
            if task == "detection":
                model = YOLO('yolov8l.pt')
                result = model(temp_file)
                
                # Process video frames
                cap = cv2.VideoCapture(temp_file)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                output_file = "output.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_file, fourcc, 30, (width, height))
                
                color_bgr, color_rgb = hex_to_bgr(color)
                
                for idx_frame in range(len(result)):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    for i in range(len(result[idx_frame].boxes.cls)):
                        if names[int(result[idx_frame].boxes.cls[i])] in selected_classes:
                            confidence = result[idx_frame].boxes.conf[i]
                            if confidence > threshold:
                                start_point_x = int(result[idx_frame].boxes.xywh[i][0]) - int(result[idx_frame].boxes.xywh[i][2] / 2)
                                start_point_y = int(result[idx_frame].boxes.xywh[i][1]) - int(result[idx_frame].boxes.xywh[i][3] / 2)
                                start_point = (start_point_x, start_point_y)
                                end_point_x = start_point_x + int(result[idx_frame].boxes.xywh[i][2])
                                end_point_y = start_point_y + int(result[idx_frame].boxes.xywh[i][3])
                                end_point = (end_point_x, end_point_y)

                                frame = cv2.rectangle(frame, start_point, end_point, color_bgr, thickness)

                                if show_confidence:
                                    frame = cv2.putText(frame, 
                                        f"{confidence:.2f}%",
                                        (end_point_x - 30, start_point_y + 12), 
                                        cv2.FONT_HERSHEY_TRIPLEX, 
                                        0.4, 
                                        color_bgr, 
                                        1)

                                if show_labels:
                                    object_name = names[int(result[idx_frame].boxes.cls[i])]
                                    frame = cv2.putText(frame, 
                                        object_name, 
                                        (start_point_x + 6, start_point_y + 12), 
                                        cv2.FONT_HERSHEY_TRIPLEX, 
                                        0.4, 
                                        color_bgr, 
                                        1)
                
                    out.write(frame)
                
                cap.release()
                out.release()
                
                with open(output_file, 'rb') as f:
                    return {"video": f.read().hex()}
                
            elif task == "segmentation":
                print("Loading YOLO segmentation model for video...")
                model = YOLO("yolov8n-seg.pt")
                result = model(temp_file)
                
                cap = cv2.VideoCapture(temp_file)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                output_file = "output.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_file, fourcc, 30, (width, height))
                
                for idx_frame in range(len(result)):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Tworzymy kopię klatki do rysowania
                    frame_with_masks = frame.copy()
                    
                    # Pobieramy maski i klasy dla aktualnej klatki
                    masks = result[idx_frame].masks
                    boxes = result[idx_frame].boxes
                    
                    # Tworzymy pustą maskę dla wszystkich obiektów
                    combined_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
                    
                    for i in range(len(masks)):
                        if i < len(boxes):
                            confidence = float(boxes[i].conf)
                            class_id = int(boxes[i].cls)
                            class_name = names[class_id]
                            
                            if class_name in selected_classes and confidence > threshold:
                                # Pobieramy maskę i konwertujemy ją na numpy array
                                mask = masks[i].data[0].cpu().numpy()
                                mask = (mask * 255).astype(np.uint8)
                                
                                # Dodajemy maskę do combined_mask
                                combined_mask = cv2.bitwise_or(combined_mask, mask)
                                
                                # Rysujemy kontur maski
                                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                cv2.drawContours(frame_with_masks, contours, -1, color_bgr, thickness)
                                
                                if show_labels:
                                    # Znajdujemy środek maski
                                    M = cv2.moments(mask)
                                    if M["m00"] != 0:
                                        cX = int(M["m10"] / M["m00"])
                                        cY = int(M["m01"] / M["m00"])
                                        cv2.putText(frame_with_masks, 
                                            class_name, 
                                            (cX - 20, cY), 
                                            cv2.FONT_HERSHEY_TRIPLEX, 
                                            0.4, 
                                            color_bgr, 
                                            1)
                    
                    # Nakładamy maskę na klatkę z przezroczystością
                    alpha = 0.3
                    overlay = frame_with_masks.copy()
                    overlay[combined_mask > 0] = color_bgr
                    cv2.addWeighted(overlay, alpha, frame_with_masks, 1 - alpha, 0, frame_with_masks)
                    
                    out.write(frame_with_masks)
                
                cap.release()
                out.release()
                
                with open(output_file, 'rb') as f:
                    return {"video": f.read().hex()}
        
        return {"error": "Unsupported file type or task"}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e)} 