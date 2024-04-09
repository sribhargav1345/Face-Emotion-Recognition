import numpy as np
import cv2
import streamlit as st
from keras.models import model_from_json
from keras.utils import img_to_array
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av

emotion_name = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

json_file = open('./models/vgg48_json.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

classifier = model_from_json(loaded_model_json)
classifier.load_weights("./models/vgg48_wt.weights.h5")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class FaceEmotionDetector(VideoProcessorBase):
    def __init__(self):
        super().__init__()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.default_expression = "Neutral"  # Set default expression

    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(img_gray, scaleFactor=1.3, minNeighbors=5)

        print("Came here")

        if len(faces) == 0:
            # If no faces detected, display default expression at the middle of the video
            label_position = (img.shape[1] // 2 - 100, img.shape[0] // 2)
            cv2.rectangle(img, (label_position[0], label_position[1] - 50), 
                          (label_position[0] + 200, label_position[1] + 50), 
                          (0, 255, 0), 2)
            cv2.putText(img, self.default_expression, label_position, 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            return cv2.rectangle
            return av.VideoFrame.from_ndarray(img, format="bgr24")

        print(len(faces))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = img_gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                prediction = classifier.predict(roi)[0]
                maxindex = int(np.argmax(prediction))
                finalout = emotion_name[maxindex]
                output = str(finalout)

                label_position = (x, y)
                cv2.putText(img, output, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return cv2.rectangle
        
        print("Number of faces detected:", len(faces)) 
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
            mode=WebRtcMode.SENDRECV,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            video_processor_factory=FaceEmotionDetector,
            async_processing=True,
        )

if __name__ == "__main__":
    main()
