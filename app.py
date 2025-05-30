import streamlit as st
import cv2
import numpy as np
#from PIL import Image
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

import platform

# Muestra la versión de Python junto con detalles adicionales
st.write("Versión de Python:", platform.python_version())

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

st.title("Batalla de Pokémon!")
#st.write("Versión de Python:", platform.python_version())
image = Image.open('Types.png')
st.image(image, width=350)
with st.sidebar:
    st.subheader("""
    Has entrado en una batalla con un pokémon salvaje. 
    Utiliza papel, tijera o piedra para combatir, y dependiendo de su
    tipo podrás tener éxito. Buena suerte!
    """)
img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
   #To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    newsize = (224, 224)
    img = img.resize(newsize)
    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Normalize the image
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(prediction)
    if prediction[0][0]>0.5:
      st.header('Papel, con Probabilidad: '+str( prediction[0][0]) +' ' +'```Es súper efectivo! Has ganado la batalla.```')
    if prediction[0][1]>0.5:
      st.header('Tijera, con Probabilidad: '+str( prediction[0][1]) +' ' +'```Han empatado la batalla.```')
    if prediction[0][2]>0.5:
     st.header('Piedra, con Probabilidad: '+str( prediction[0][2]) +' ' +'```No es muy efectivo... Has perdido la batalla.```')


