#!/usr/bin/python3
# coding=utf-8
# 主进程
from multiprocessing import Process
from autocar import wheel
from autocar import controller
from autocar import ultrasonic
from autocar import dd


if __name__=="__main__":
    p1 = Process(target=wheel.standby,args=(dd,),name='wheel')
    p2 = Process(target=controller.webconsole,args=(dd,),name='controller')
    p3 = Process(target=ultrasonic.standby,args=(dd,),name='ultrasonic')

    p1.daemon = True
    p2.daemon = True
    p3.daemon = True
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()

    print("offline")