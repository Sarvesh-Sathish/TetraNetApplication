from flask import Flask, render_template, Response, request, redirect
import cv2
import os
from PIL import Image, ImageOps
from numpy import asarray
import numpy as np
from azure_get_unet import get_mask
import requests
import azure_get_atmosphere



video = cv2.VideoCapture(0)
app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = 'images'
print(os.listdir('uploads/images'))
response = requests.get('http://67515655-f00a-44a0-a447-22a76351d991.eastus.azurecontainer.io/score')
print('response', response.json())
print(azure_get_atmosphere.run_ANN())



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



@app.route('/')
def home():
    print('hi')
    return render_template("index.html")



@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/another_page.html', methods=['GET', 'POST'])
def another_page():
    print(request.method)
    if request.method == 'GET':
        return render_template('another_page.html')
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            image.save('uploads/images/test.png')
            print(type(image), 'image saved')

    return render_template('another_page.html')


if __name__ == '__main__':
    app.run(debug=True)






