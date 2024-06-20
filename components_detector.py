import tensorflow as tf
import streamlit as st
import numpy as np
import cv2
from PIL import Image
import tensorflow_hub as hub
from labels import LABELS

model = None
detector = None
min_confidence = 0.5

COLORS = np.random.uniform(0, 255, size=(91, 3))

@st.cache_resource
def load_model():
    # Load the pre-trained SSD MobileNet model
    detector = hub.load("https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v2/TensorFlow2/ssd-mobilenet-v2/1")
    return detector

def detect_objects(image, detector):
    # Convert the image to a numpy array
    image_np = np.array(image)
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis,...]

    # Run the model
    detections = detector(input_tensor)

    detection_classes = detections['detection_classes'][0].numpy().astype(np.int64)
    detection_scores = detections['detection_scores'][0].numpy()
    detection_boxes = detections['detection_boxes'][0].numpy()

    detected_objects = []
    height, width, _ = image_np.shape

    for i , class_idx in enumerate(detection_classes):
        if detection_scores[i] >= min_confidence:
            class_name = LABELS.get(class_idx, 'N/A')
            if class_name != 'N/A':
                color = COLORS[class_idx]
                box = detection_boxes[i] * [height, width, height, width]
                detected_objects.append((class_name, detection_scores[i], box , color))

    return detected_objects

def draw_boxes(image, detected_objects):
    image_np = np.array(image)
    for obj in detected_objects:
        class_name, score, box , color = obj
        y1, x1, y2, x2 = box.astype(int)
        image_np = cv2.rectangle(image_np, (x1, y1), (x2, y2), color, 2)
        image_np = cv2.putText(image_np, f"{class_name} ({score:.2f})", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return Image.fromarray(image_np)