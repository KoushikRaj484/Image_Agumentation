import streamlit as st 
import cv2
import numpy as np
from PIL import Image
import random
import zipfile
import io

def Translation(img1):
    tx = np.random.randint(0,150)
    ty = np.random.randint(0,200)
    t = np.array([[1,0,tx],[0,1,ty]]).astype("float32")
    im  = cv2.warpAffine(img1,t,[img1.shape[1],img1.shape[0]])
    return im
def Grayscale(img1):
    gr = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    return gr
def Rotate(img1):
    r = np.random.randint(-180,180)
    h, w = img1.shape[:2]
    im = cv2.getRotationMatrix2D((w // 2, h // 2), r, 1)
    im  = cv2.warpAffine(img1,im,[w,h])
    return im
def Flip_Horizontally(img1):
    fh = cv2.flip(img1, 1)
    return fh
def Flip_Vertically(img1):
    return cv2.flip(img1, 0)
def Shearing(img1):
    sx = np.random.rand()
    sy = np.random.rand()
    t = np.array([[1,sx,0],[sy,1,0]]).astype("float32")
    im  = cv2.warpAffine(img1,t,[img1.shape[1],img1.shape[0]])
    return im
def Cropping(img1):
    y1 = np.random.randint(0,img1.shape[0]//2) 
    y2 = np.random.randint(img1.shape[0]//2,img1.shape[0]) 
    x1 = np.random.randint(0,img1.shape[1]//2) 
    x2 = np.random.randint(img1.shape[1]//2,img1.shape[1]) 
    return img1[y1:y2,x1:x2]

st.title("Welcome to Image Agumentation tools")
up_file = st.file_uploader("Choose an image with png, jpg, jpeg.", type=["png", "jpg", "jpeg"])

if st.button("Upload"): 
    if up_file is not None:
        st.image(up_file)
        st.success("Image uploaded successfully!")
    else:
        st.warning("Please upload an image before clicking upload.")

num = int(st.number_input("Insert a number", min_value=1, step=1))
st.write("The current number is ", num)

l1 = ["Translation","Grayscale","Rotate","Flip Horizontally","Flip Vertically","Shearing","Cropping"]
c = st.multiselect("Select",l1)
l=[]
for i in c:
    l.append(i.replace(" ","_"))


st.markdown("---")
images = []
if st.button("Generate images"): 
    img = np.array(Image.open(up_file))
    for i in range(0,num):
        img2 = img.copy()
        for j in l:
            j = globals()[j]  
            img2 = j(img2)

        img2=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
        images.append(img2)
    st.success("Generate Successfull")
    
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, "w") as zip_file:
    for idx, img in enumerate(images):
        is_success, buffer = cv2.imencode(".jpg", img)
        if is_success:
            zip_file.writestr(f"augmented_{idx+1}.jpg", buffer.tobytes())

zip_buffer.seek(0)
if st.download_button(
    label="Download ZIP on Augmented Images",
    data=zip_buffer,
    file_name="augmented_images.zip",
    mime="application/zip"
  ):
    st.success("Successfully Download")