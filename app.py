from flask import Flask, render_template, Response, request, redirect, send_file
import cv2
import os
from PIL import Image, ImageOps
from numpy import asarray
import numpy as np
from azure_get_unet import get_mask
import requests
import azure_get_atmosphere
import firespread
import io



video = cv2.VideoCapture(0)
app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = 'images'
print(os.listdir('uploads/images'))
response = requests.get('http://67515655-f00a-44a0-a447-22a76351d991.eastus.azurecontainer.io/score')
print('response', response.json())

# arr = firespread.img_dir_to_arr('uploads/images/test.png')
# print(arr)
# image = Image.fromarray(arr)
# image.save('uploads/images/lets-see.png')


def gen_frames():
    while True:
        success, frame = video.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def save_img(image_obj):
    ORIGINAL_IMAGE_DIR = 'static/images/uploads/original_img.png'
    image_obj.save(ORIGINAL_IMAGE_DIR)
    return ORIGINAL_IMAGE_DIR

def save_mask(image_mask_np, shape):
    MASK_IMAGE_DIR = 'static/images/uploads/mask.png'
    mask = Image.fromarray(image_mask_np)
    mask = mask.resize((shape[1], shape[0]))
    print('mask reshaped to' + str(shape[0]) + 'x' + str(shape[1]))
    mask.save(MASK_IMAGE_DIR)
    return MASK_IMAGE_DIR

def get_img_shape(img_dir):
    img = Image.open(img_dir)
    img = asarray(img)
    return img.shape

def get_prediction_frame(mask_obj_arr):
    mask_obj_arr = np.array(mask_obj_arr)
    ret, mask_encoded = cv2.imencode('.jpg', mask_obj_arr)
    mask_encoded = mask_encoded.tobytes()
    return (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + mask_encoded + b'\r\n')



@app.route('/')
def home():
    print('hi')
    return render_template("index.html")

@app.route('/show_prediction')
def show_prediction(mask_obj_arr):
    return Response(get_prediction_frame(mask_obj_arr), mimetype='image/png; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/original_image')
def original_image():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/another_page.html', methods=['GET', 'POST'])
def another_page():
    print(request.method)
    saved_dir =''
    mask_dir = ''
    if request.method == 'GET':
        return render_template('another_page.html')
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            saved_dir = save_img(image)
            shape = get_img_shape(saved_dir)
            print(shape)
            # now we will also get the segmentation mask for the original image
            mask = get_mask(saved_dir)
            show_prediction(mask)
            mask_dir = save_mask(mask, shape)

    return render_template('another_page.html', original_image=saved_dir)




if __name__ == '__main__':
    app.run(debug=True)






