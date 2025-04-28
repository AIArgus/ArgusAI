import streamlit as st
from ultralytics import YOLO
import numpy as np
import cv2


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


names_list =  [name for name in names.values()]

def hex_to_bgr(value):
    value = value.lstrip('#')
    lv = len(value)
    rgb_value = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    r_value, g_value, b_value = rgb_value
    bgr_value = (b_value, g_value, r_value)
    rgb_value = (r_value, g_value, b_value)
    return bgr_value, rgb_value


def detect_objects_on_image():
    detection_model = YOLO('yolov8l.pt')
    image = read_image_bytes(my_upload, 'detection')
    result = detection_model.predict(image)
    number_of_objects = len(result[0].boxes.cls)
    for i in range(0, number_of_objects):   # ta petla dodaje bbox wykrytych obiektów w danej klatce
        if  names[int(result[0].boxes.cls[i])] in st.session_state['kind_of_objects']:
            confidence = result[0].boxes.conf[i]
            if confidence > threshold:
                start_point_x = int(result[0].boxes.xywh[i][0]) - \
                                int(result[0].boxes.xywh[i][2] / 2)
                start_point_y = int(result[0].boxes.xywh[i][1]) - \
                                int(result[0].boxes.xywh[i][3] / 2)

                start_point = (start_point_x, start_point_y)

                end_point_x = start_point_x + int(result[0].boxes.xywh[i][2])
                end_point_y = start_point_y + int(result[0].boxes.xywh[i][3])

                end_point = (end_point_x, end_point_y)

                image = cv2.rectangle(image, start_point, end_point, color_value_rgb, thickness_line)

                if are_confs:
                    confidence = result[0].boxes.conf[i]

                    image = cv2.putText(image, 
                                str(confidence)[9:11] + "%",
                                (end_point_x -30, start_point_y + 12), 
                                fontFace=cv2.FONT_HERSHEY_TRIPLEX, 
                                fontScale=0.4, 
                                color=(0, 255, 0), 
                                thickness=1)

                if are_labels == True:
                    object_name = names[int(result[0].boxes.cls[i])]

                    image = cv2.putText(image, 
                            object_name, 
                            (start_point_x +6, start_point_y + 12), 
                            fontFace=cv2.FONT_HERSHEY_TRIPLEX, 
                            fontScale=0.4, 
                            color=(0, 255, 0), 
                            thickness=1)
                

    st.image(image, use_column_width=True)


def detect_objects_on_video():
    tempfile_name = 'tempfile.mp4'

    with open(tempfile_name, 'wb') as file:
        file.write(my_upload.getbuffer())

    detection_model = YOLO('yolov8l.pt')
    
    with st.spinner("Processing video..."):
        result = detection_model(tempfile_name)


    vidcap = cv2.VideoCapture(tempfile_name)
    width  = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 35, (width,  height))

    is_success = True

    idx_frame = 0
    while is_success:   # ta pętla przetwarza klatki
        is_success, frame = vidcap.read()
        if is_success == False:
            break
        
        number_of_objects = len(result[idx_frame].boxes.cls)

        for i in range(0, number_of_objects):   # ta petla dodaje bbox wykrytych obiektów w danej klatce
            if  names[int(result[idx_frame].boxes.cls[i])] in st.session_state['kind_of_objects']:
                confidence = result[idx_frame].boxes.conf[i]
                if confidence > threshold:
                    start_point_x = int(result[idx_frame].boxes.xywh[i][0]) - \
                                    int(result[idx_frame].boxes.xywh[i][2] / 2)
                    start_point_y = int(result[idx_frame].boxes.xywh[i][1]) - \
                                    int(result[idx_frame].boxes.xywh[i][3] / 2)

                    start_point = (start_point_x, start_point_y)

                    end_point_x = start_point_x + int(result[idx_frame].boxes.xywh[i][2])
                    end_point_y = start_point_y + int(result[idx_frame].boxes.xywh[i][3])

                    end_point = (end_point_x, end_point_y)

                    frame = cv2.rectangle(frame, start_point, end_point, color_value_bgr, thickness_line)

                    if are_confs:
                        frame = cv2.putText(frame, 
                                    str(confidence)[9:11] + "%",
                                    (end_point_x -30, start_point_y + 12), 
                                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, 
                                    fontScale=0.4, 
                                    color=(0, 255, 0), 
                                    thickness=1)

                    if are_labels == True:
                        object_name = names[int(result[idx_frame].boxes.cls[i])]

                        frame = cv2.putText(frame, 
                                object_name, 
                                (start_point_x +6, start_point_y + 12), 
                                fontFace=cv2.FONT_HERSHEY_TRIPLEX, 
                                fontScale=0.4, 
                                color=(0, 255, 0), 
                                thickness=1)

        out.write(frame)
        idx_frame += 1
    
    out.release()

    video_file = open('output.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)


def read_image_bytes(image_bytes, task):
    nparr = np.frombuffer(image_bytes.read(), np.uint8)
    print(nparr.shape)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if task != "segmentation":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def segment_on_video(my_upload):
    tempfile_name = 'tempfile.mp4'

    with open(tempfile_name, 'wb') as file:
        file.write(my_upload.getbuffer())

    model = YOLO("yolov8n-seg.pt")
    
    with st.spinner("Processing video..."):
        result = model(tempfile_name)


    vidcap = cv2.VideoCapture(tempfile_name)
    width  = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 35, (width,  height))


    for idx_frame in range(len(result)):   # ta pętla przetwarza klatki

        result[idx_frame].save('seg_output.png')
        image = cv2.imread('seg_output.png')

        out.write(image)

    out.release()

    st.video('output.mp4')


if 'kind_of_objects' not in st.session_state:
    st.session_state['kind_of_objects'] = []

if 'detect_object_button' not in st.session_state:
    st.session_state['detect_object_button'] = False


st.set_page_config(initial_sidebar_state='collapsed')
st.title("Computer Vision website")
st.text("Authors: ")
st.text("- Igor Ćwiertnia")
st.text("- Robert Walery")

task = st.selectbox(options= ['Object detection', 'Segmentation'], label="Choose task")

if task == 'Object detection':
    st.sidebar.title("Settings")
    are_labels = st.sidebar.toggle("Show labels")
    are_confs = st.sidebar.toggle("Show confidence")
    threshold = st.sidebar.slider("Set threshold", 
                                        min_value=0.1, 
                                        max_value=1.0, 
                                        value=0.25, 
                                        step=0.1)

    color_value_hex = st.sidebar.color_picker("Choose bounding boxes' color", 
                                            '#B9282B')
    color_value_bgr, color_value_rgb = hex_to_bgr(color_value_hex)

    thickness_line = st.sidebar.slider("Choose thickness of bbx's lines", 
                                        min_value=1, 
                                        max_value=5, 
                                        value=2, 
                                        step=1)

    my_upload = st.file_uploader("Upload a media")

    if my_upload:
        idx_slash = my_upload.type.index('/')
        media_type = my_upload.type[:idx_slash]

        if media_type == "image":
            st.image(my_upload, use_column_width=True)
        else:
            st.video(my_upload, autoplay=True, muted=True)
        
        detect_clicked = st.button("Detect object")

        if detect_clicked:
            st.session_state['detect_object_button'] = True

        if st.session_state['detect_object_button']:
            st.session_state['kind_of_objects'] = st.multiselect(label="Choose kind of objects to detection", options=names_list)

        if st.session_state['kind_of_objects']:
            if media_type == "image":
                detect_objects_on_image()
            else:
                detect_objects_on_video()
else:
    model = YOLO("yolov8n-seg.pt")

    my_upload = st.file_uploader("Upload a media")
    if my_upload:
        idx_slash = my_upload.type.index('/')
        media_type = my_upload.type[:idx_slash]

        if media_type == "image":
            st.image(my_upload, use_column_width=True)
            image = read_image_bytes(my_upload, 'segmentation')
            result = model(image)

            result[0].save('seg_output.png')
            st.image('seg_output.png', use_column_width=True)
        else:
            st.video(my_upload, autoplay=True, muted=True)

            segment_on_video(my_upload)

