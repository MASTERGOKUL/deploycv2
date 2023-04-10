# to run streamlit put it in terminal `streamlit run app.py`
# refer api/element documentation : https://docs.streamlit.io/library/api-reference
import streamlit as st  # importing stream lit after `pip install streamlit`
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO

# to change the title and icon
st.set_page_config(page_title="Cv2", page_icon="📷", layout="wide", initial_sidebar_state="collapsed", menu_items=None)
st.title("Deploy cv2")  # like h1 tag
img = st.file_uploader("Upload your image to see the result", type=['jpg', 'png'])

# to make html use `st.markdown("""<html code here/>""")`
# Add 'before' and 'after' columns
if img is not None:
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        st.markdown('<p style="text-align: center;">Before</p>', unsafe_allow_html=True)
        st.image(img, use_column_width='auto')  # to show in original resolution `use_column_width ='auto'`
        image = Image.open(img)
        # Add conditional statements to take the user input values
        with col2:
            st.markdown('<p style="text-align: center;">After</p>', unsafe_allow_html=True)
            st.sidebar.subheader("Select the value to change Output")
            model = st.sidebar.radio("select the model to change output",['FaceDetection','EyeDetection'])
            if(model=='FaceDetection'):
                faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            else:
                faceCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
            img=np.array(image.convert('RGB'))
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = faceCascade.detectMultiScale(imgGray, 1.1, 4)
            for (x, y, w, h) in face:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            st.image(img)#OUTPUT OCCURED
            # Save the modified image to a bytes buffer
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            buffered = BytesIO()
            cv2.imwrite("image.jpg", img)

            # Read the saved image file as bytes
            with open("image.jpg", "rb") as f:
                img_bytes = f.read()
            b64 = base64.b64encode(img_bytes).decode()
            #download button
            st.markdown(""" <style> #a {
            justify-content:end;
            font-family:"Source Sans Pro", sans-serif;
            padding:5px;
            text-decoration:none;
            color:#FF4B4B;
            border:2px solid #FF4B4B;
            border-radius:5px;
                } 
                #a:hover{
                padding:5px;
            text-decoration:none;
                color:#fff;
                background-color:#FF4B4B;
                }
                </style> """, unsafe_allow_html=True)
            href = f'<a id="a" href="data:file/jpg;base64,{b64}" download="image.jpg">Download Output Image</a>'
            st.markdown(href, unsafe_allow_html=True)
