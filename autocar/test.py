from flask import Flask ,render_template,Response
import cv2

class VC(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        r,img = self.video.read()
        ret,jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

app = Flask(__name__)

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed', methods=['GET'])
def video_feed():
    return Response(gen(VC()),mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=5000)
 #https: // www.cnblogs.com / arkenstone / p / 7159615.html
