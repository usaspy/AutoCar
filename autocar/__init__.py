#-*- coding: UTF-8 -*-
#指令通道
from multiprocessing import Process,Manager

m = Manager()
dd = m.dict()

#"目标对象" >>"优先级" "来源对象" "指令"