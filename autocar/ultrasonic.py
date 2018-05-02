#!/usr/bin/python3
# coding=utf-8
# 超声波测距系统
#  0.3 米 =近进告警  0.1米=抵近停止
# 具备下列功能：
#1.实时采集当前正前方（7.5）的障碍物距离，如果小于0.1米立即发送停止前进的命令
#2.同时从左至右采集四个方向的距离2.5、4、8、9.5的距离（探测完成后回到6=正前方）
#3.如果存在无障碍的方向( >0.3米)，即随机从几个方向点上选择一个执行程序转弯（转弯完成后，超声波检测恢复），之后继续行走并执行步骤1
#4.如果都有障碍，表示无法绕过，则控制车辆倒退1秒，继续执行步骤2
import RPi.GPIO as GPIO
import time
from random import choice

STATUS = "OK" #一切正常

GPIO.setmode(GPIO.BOARD)
#SG90马达
sg90_pin = 8

direction1=2.5
direction2=4
direction3=8
direction4=9.5
direction0=6 #正前方

#超声波
echo_pin = 13
trig_pin=11

alert_dist=0.4 #0.3米
stop_dist=0.2 #0.1米

# 转向马达初始化:
GPIO.setup(sg90_pin, GPIO.OUT, initial=False)
p = GPIO.PWM(sg90_pin, 50)

#超声波初始化
GPIO.setup(trig_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(echo_pin, GPIO.IN)

#系统复位
def rest():
    GPIO.cleanup()

#转向到一个指定角度并开始测距，返回一个距离值
def get_distance(direction):
    #先转向指定角度
    p.ChangeDutyCycle(direction)
    time.sleep(0.5)

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

    return direction,distance

#超声波子系统准备就绪，等待指令
def standby(dd):
    p.start(direction0)  # 超声波方向对正前方
    time.sleep(0.5)
    while True:
        try:
            dir,dist = get_distance(direction0)
            if dist <= stop_dist:
                dd['CMD_WHEEL'] = 'stop'
                dirs = []
                for direct in [direction1,direction2,direction3,direction4]:
                    dir,dist = get_distance(direct)
                    if dist > alert_dist:
                        dirs.append(direct)
                #如果四个角度都太近，则后退一段距离重新测试
                if dirs.__len__() == 0:
                    dd['CMD_WHEEL'] = 'backaway'
                    time.sleep(1)
                    dd['CMD_WHEEL'] = 'stop'
                else:
                    fin = choice(dirs)
                    print(fin)
                    if fin > direction0:
                        dd['CMD_WHEEL'] = 'turn_left'
                        time.sleep(1)
                        dd['CMD_WHEEL'] = 'stop'
                    if fin < direction0:
                        dd['CMD_WHEEL'] = 'turn_right'
                        time.sleep(1)
                        dd['CMD_WHEEL'] = 'stop'

        except Exception as e:
            continue
        finally:
            time.sleep(0.2)