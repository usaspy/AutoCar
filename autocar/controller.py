#!/usr/bin/python3
# coding=utf-8
# 控制器
# 接受来自使用者的命令，命令来源： web URL、红外线、蓝牙
# 手机控制 web方式通过ajax调用控制运行
import time
import datetime
from flask import Flask,render_template,request,jsonify
from flask import url_for

app = Flask(__name__)

def webconsole(dd):
        @app.route('/console', methods=['GET'])
        def console():
                return render_template('console.html')

        @app.route('/wheel', methods=['GET'])
        def wheel_action():
                action = request.values.get("action")
                dd['CMD_WHEEL'] = action
                return jsonify({'result': "success"})

        app.run(host="192.168.0.9", port=80, debug=False)
import autocar.webconsole