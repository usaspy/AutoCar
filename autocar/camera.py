#!/usr/bin/python3
# coding=utf-8
# 摄像头子系统
# 具备下列功能
#1.启动后处于待机状态
#2.# 当客户端发起监控请求，启动摄像头拍照并实时传送给客户端浏览器

from flask import Flask ,render_template,Response
import cv2

app = Flask(__name__)

class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    #实时获取图像帧
    def get_frame(self):
        re,img = self.video.read()
        ret,jpeg = cv2.imencode('.jpg',img)
        return jpeg.tobytes()

def CameraVideo(dd):
    @app.route('/screen', methods=['GET'])
    def screen():
        return render_template('screen.html')

    @app.route('/video_source', methods=['GET'])
    def video_source():
        return Response(gen(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")

    def gen(camera):
        while True:
            frame = camera.get_frame()
            #使用生成器yield
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    app.run(host="192.168.0.9", debug=False, port=5000)