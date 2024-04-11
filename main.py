import numpy as np
import cv2
import streamlit as st
from keras.models import model_from_json
from keras.utils import img_to_array
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

emotion_name = {0: 'Happy', 1: 'Disgust', 2: 'Fear', 3: 'Surprise', 4: 'Sad', 5: 'Neutral', 6: 'Angry'}

from torchvision.models import regnet_y_1_6gf

num_classes = 7
model = regnet_y_1_6gf(weights='IMAGENET1K_V2')
model.to(torch.device('cpu'))                       # Keep cuda here, if your computer supports

model.load_state_dict(torch.load("models\\regnet_y_1.6gf_emotion_detection.pth", map_location=torch.device('cpu')))  # Keep cuda here, if your computer supports
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def callback(frame):
    img = frame.to_ndarray(format="bgr24")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        face=img[y:y+h, x:x+w]
        image_pil = Image.fromarray((face * 255).astype(np.uint8))
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        # Apply transformations to the image
        image_tensor = transform(image_pil).unsqueeze(0) 
        with torch.no_grad():
            outputs = model(image_tensor)

        # Get predictions
        _, predicted = torch.max(outputs, 1)
        print(emotion_name[predicted.item()])
        try:
            cv2.putText(img, emotion_name[predicted.item()], (x,y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255), thickness=2)
        except Exception as e:
            print(e)  
    # img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    st.title("Real Time Face Emotion Detection Application")
    activities = ["Home", "Webcam Emotion Detection"]
    choice = st.sidebar.selectbox("Select Activity", activities)
    st.sidebar.markdown("Developed by Bhargav and Nikhil")
    
    if choice == "Home":
        st.write("""
                 The application has two functionalities.
                 1. Real-time face detection using webcam feed.
                 2. Real-time face emotion recognition.
                 """)

    elif choice == "Webcam Emotion Detection":
        st.header("Webcam Live Feed")
        st.write("Click on start to use the webcam and detect your face emotion")

        webrtc_streamer(
            key="example",
            video_frame_callback=callback
        )

if __name__ == "__main__":
    main()
