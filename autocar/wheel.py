#!/usr/bin/python3
# coding=utf-8
# 行走子系统
# 具备下列功能：
# 1.系统激活，行走子系统进入准备状态，等待接收控制命令
# 2.用户通过URL发送控制命令，支持前进、倒退、左转、右转、停车、打火等控制操作
# 3.支持碰撞避免，当前方有障碍物时，会越过用户的控制指令即时停车。
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

in1 = 29  # in1和in2一同控制左侧轮子运动
in2 = 31
in3 = 33  # in3和in4一同控制右侧侧轮子运动
in4 = 35
enda = 40  # 左轮使能
endb = 37  # 右轮使能，貌似只要左轮使能了两边都能转


#打火，行走系统初始化
def fire():
    GPIO.setup(in1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(in2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(in3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(in4, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(enda, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(endb, GPIO.OUT, initial=GPIO.LOW)

#熄火
def misfire():
    GPIO.cleanup()

#左侧轮子向前运动
def __left_forward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enda,GPIO.HIGH)

#左侧轮子向后运动
def __left_backaway():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(enda,GPIO.HIGH)

#左侧轮子停止
def __left_stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enda,GPIO.HIGH)

#右侧轮子向前运动
def __right_forward():
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        GPIO.output(endb,GPIO.HIGH)

#右侧轮子向后运动
def __right_backaway():
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        GPIO.output(endb,GPIO.HIGH)

#右侧轮子停止
def __right_stop():
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        GPIO.output(endb,GPIO.HIGH)

#前进
def forward():
    __left_forward()
    __right_forward()

#后退
def backaway():
    __left_backaway()
    __right_backaway()

#左转
def turn_left():
    __left_backaway()
    __right_forward()

#右转
def turn_right():
    __left_forward()
    __right_backaway()

#停车
def stop():
    __left_stop()
    __right_stop()

#行走子系统准备就绪，等待指令
def standby(dd):
    fire()
    while True:
        print(dd)
        try:
            if dd['CMD_WHEEL'] == 'forward':
                forward()
            elif dd['CMD_WHEEL'] == 'backaway':
                backaway()
            elif dd['CMD_WHEEL'] == 'turn_left':
                turn_left()
            elif dd['CMD_WHEEL'] == 'turn_right':
                turn_right()
            elif dd['CMD_WHEEL'] == 'stop':
                stop()
            elif dd['CMD_WHEEL'] == 'misfire':
                misfire()
            elif dd['CMD_WHEEL'] == 'fire':
                fire()  #发动
            time.sleep(0.01)
        except Exception as e:
            continue