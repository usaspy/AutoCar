# 将音频命令转成HTTP URL命令发送到AutoCar模块
import urllib
import urllib.request
from urllib.parse import urlencode

def sendCMD2AutoCar(cmd):
    print(cmd)
    for i in cmd:
        if  i.find('前进') != -1:
            sendurl("forward")
            break
        if i.find('停') != -1:
            sendurl("stop")
            break
        if i.find('后退') != -1:
            sendurl("backaway")
            break
        if i.find('左转') != -1:
            sendurl("turn_left")
            break
        if i.find('右转') != -1:
            sendurl("turn_right")
            break

def sendurl(s):
    value = {'action':s}
    url = 'http://192.168.0.9/wheel?%s'% urlencode(value)
    print(url)
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req).read()
    return resp