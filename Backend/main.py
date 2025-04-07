from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import numpy as np
import cv2
import os
from typing import List
import json

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
    if task != "segmentation":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

@app.get("/api/class-names")
async def get_class_names():
    return {"class_names": names_list}

@app.post("/api/detect")
async def detect_objects(
    file: UploadFile = File(...),
    task: str = "detection",
    selected_classes: List[str] = None,
    threshold: float = 0.25,
    show_labels: bool = True,
    show_confidence: bool = True,
    color: str = "#B9282B",
    thickness: int = 2
):
    try:
        if selected_classes is None:
            selected_classes = names_list

        content = await file.read()
        file_type = file.content_type.split('/')[0]
        print(f"Processing {file_type} file: {file.filename}, size: {len(content)} bytes")

        if file_type == "image":
            try:
                image = read_image_bytes(content, task)
                print(f"Successfully read image with shape: {image.shape}")
                
                if task == "detection":
                    print("Loading YOLO model...")
                    model = YOLO('yolov8l.pt')
                    print("Running detection...")
                    result = model.predict(image)
                    print(f"Detection complete. Found {len(result[0].boxes.cls)} objects")
                    
                    color_bgr, color_rgb = hex_to_bgr(color)
                    
                    for i in range(len(result[0].boxes.cls)):
                        if names[int(result[0].boxes.cls[i])] in selected_classes:
                            confidence = result[0].boxes.conf[i]
                            if confidence > threshold:
                                start_point_x = int(result[0].boxes.xywh[i][0]) - int(result[0].boxes.xywh[i][2] / 2)
                                start_point_y = int(result[0].boxes.xywh[i][1]) - int(result[0].boxes.xywh[i][3] / 2)
                                start_point = (start_point_x, start_point_y)
                                end_point_x = start_point_x + int(result[0].boxes.xywh[i][2])
                                end_point_y = start_point_y + int(result[0].boxes.xywh[i][3])
                                end_point = (end_point_x, end_point_y)

                                image = cv2.rectangle(image, start_point, end_point, color_rgb, thickness)

                                if show_confidence:
                                    image = cv2.putText(image, 
                                        f"{confidence:.2f}%",
                                        (end_point_x - 30, start_point_y + 12), 
                                        cv2.FONT_HERSHEY_TRIPLEX, 
                                        0.4, 
                                        (0, 255, 0), 
                                        1)

                                if show_labels:
                                    object_name = names[int(result[0].boxes.cls[i])]
                                    image = cv2.putText(image, 
                                        object_name, 
                                        (start_point_x + 6, start_point_y + 12), 
                                        cv2.FONT_HERSHEY_TRIPLEX, 
                                        0.4, 
                                        (0, 255, 0), 
                                        1)

                    print("Converting image for response...")
                    _, buffer = cv2.imencode('.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                    return {"image": buffer.tobytes().hex()}
                
                elif task == "segmentation":
                    model = YOLO("yolov8n-seg.pt")
                    result = model(image)
                    result[0].save('seg_output.png')
                    with open('seg_output.png', 'rb') as f:
                        return {"image": f.read().hex()}
            
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
                                        (0, 255, 0), 
                                        1)

                                if show_labels:
                                    object_name = names[int(result[idx_frame].boxes.cls[i])]
                                    frame = cv2.putText(frame, 
                                        object_name, 
                                        (start_point_x + 6, start_point_y + 12), 
                                        cv2.FONT_HERSHEY_TRIPLEX, 
                                        0.4, 
                                        (0, 255, 0), 
                                        1)
                
                    out.write(frame)
                
                cap.release()
                out.release()
                
                with open(output_file, 'rb') as f:
                    return {"video": f.read().hex()}
                
            elif task == "segmentation":
                model = YOLO("yolov8n-seg.pt")
                result = model(temp_file)
                
                cap = cv2.VideoCapture(temp_file)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                output_file = "output.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_file, fourcc, 30, (width, height))
                
                for idx_frame in range(len(result)):
                    result[idx_frame].save('seg_output.png')
                    frame = cv2.imread('seg_output.png')
                    out.write(frame)
                
                cap.release()
                out.release()
                
                with open(output_file, 'rb') as f:
                    return {"video": f.read().hex()}
        
        return {"error": "Unsupported file type or task"}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": str(e)} 