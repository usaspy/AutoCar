#!/usr/bin/python3
# coding=utf-8
# 超声波测距系统
#  0.3 米 =近进告警  0.1米=抵近停止
# 具备下列功能：
#1.实时采集当前正前方（7.5）的障碍物距离，如果小于0.1米立即发送停止前进的命令
#2.同时从左至右采集四个方向的距离4.5、6、9、10.5的距离（探测完成后回到7.5正前方）
#3.如果存在无障碍的方向( >0.3米)，即随机从几个方向点上选择一个执行转弯程序（转弯完成后，超声波检测恢复），之后继续行走并执行步骤1
#4.如果都有障碍，表示无法绕过，则控制车辆倒退1秒，继续执行步骤2
import RPi.GPIO as GPIO
import time

STATUS = "OK" #一切正常

GPIO.setmode(GPIO.BOARD)
#SG90马达
sg90_pin = 8

direction1=4.5
direction2=6
direction3=9
direction4=10.5
direction0=7.5 #正前方

#超声波
echo_pin = 13
trig_pin=11

alert_dist=0.3 #0.3米
stop_dist=0.1 #0.1米

#转向马达初始化:
GPIO.setup(sg90_pin, GPIO.OUT, initial=False)
p = GPIO.PWM(sg90_pin, 50)
p.start(direction0)  #超声波对正前方

#超声波初始化
GPIO.setup(trig_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(echo_pin, GPIO.IN)

#系统复位
def rest():
    GPIO.cleanup()

#转向到一个指定角度并开始测距，返回一个距离值
def __distance(direction):
    #先转向指定角度
    p.ChangeDutyCycle(direction)
    time.sleep(0.02)

    #开始测距
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.0001)

    GPIO.output(trig_pin, GPIO.LOW)
    #改成事件监听更省资源
    while GPIO.input(echo_pin) == GPIO.LOW:
        pass
    starttime = time.time()
    while GPIO.input(echo_pin) == GPIO.HIGH:
        pass
    endtime = time.time()
    distance = 340 * (endtime - starttime) / 2
    print("direction:",direction,"   distance:", distance)

    return distance

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