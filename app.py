from flask import Flask, render_template, Response, request
import cv2

video = cv2.VideoCapture(0)
app = Flask(__name__)


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
    return render_template("index.html")



@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/another_page.html', methods=['GET', 'POST'])
def another_page():

    if request.method == 'GET':
        return render_template('another_page.html')


if __name__ == '__main__':
    app.run(debug=True)


