import tm1638,time
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))
tm.show("--------")

if tm.keys()!=1: import liesi

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Jorpakko', 'Juhannusyona')
        count=0
        while not sta_if.isconnected():
            time.sleep(0.5)
            count+=1
            if count>20:
                tm.show(" NO NET ")
                time.sleep(0.5)
                return
    print('IF network config:', sta_if.ifconfig())

do_connect() 

def do_not_connect():
    import network
    ap_if = network.WLAN(network.AP_IF)
    print('AP network config:', ap_if.ifconfig())
    ap_if.active(False)
    print('AP network config:', ap_if.ifconfig())
    
import gc
gc.collect()

import esp
esp.osdebug(None)

import os
print(os.listdir())

def ls():
    print(os.listdir())

import webrepl
webrepl.start()

do_not_connect()

tm.show("EEEEEEEE")





