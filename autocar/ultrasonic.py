#!/usr/bin/python3
# coding=utf-8
# 超声波测距
import RPi.GPIO as GPIO
import atexit
import time

atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BOARD)
#SG90马达
used_pin1 = 8
#超声波
echo = 13
trig=11

#测距系统初始化
def init():
    #转向马达初始化:
    GPIO.setup(used_pin1, GPIO.OUT, initial=False)
    p = GPIO.PWM(used_pin1, 50)
    p.start(7.5)  #超声波初始角度

    #超声波初始化
    GPIO.setup(trig, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(echo, GPIO.IN)

#转向一个角度开始测距 PWM在2.5~12.5
def __distance(p,PWM):
    print("starting...")
    #先转向指定角度
    p.ChangeDutyCycle(PWM)
    time.sleep(0.02)

    #开始测距
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.0001)

    GPIO.output(trig, GPIO.LOW)
    #改成事件监听更省资源
    while GPIO.input(echo) == GPIO.LOW:
        pass
    starttime = time.time()
    while GPIO.input(echo) == GPIO.HIGH:
        pass
    endtime = time.time()
    distance = 340 * (endtime - starttime) / 2
    print("distance:", distance)

    #如果距离小于1分米报警
    if distance < 0.1:
        return "Alarm"
    else:
        return "OK"

#超声波子系统准备就绪，等待指令
def standby(dd):
    while True:
        try:
            if dd['x'] != None:
                print(dd['x'])
            else:
                print("nothing")
            time.sleep(0.01)
        except Exception as e:
            continue