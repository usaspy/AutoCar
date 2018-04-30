#!/usr/bin/python3
# coding=utf-8
# 主进程
from multiprocessing import Process
from autocar import wheel
from autocar import controller
from autocar import ultrasonic
from autocar import dd   #控制通道  进程间数据共享


if __name__=="__main__":
    p1 = Process(target=wheel.standby,args=(dd,),name='wheel')  #行走系统
    p2 = Process(target=controller.webconsole,args=(dd,),name='controller') #用户操纵系统
    p3 = Process(target=ultrasonic.standby,args=(dd,),name='ultrasonic') #超声波测距系统

    p1.daemon = True
    p2.daemon = True
    p3.daemon = True
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()

    print("系统停机...")