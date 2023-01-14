
menyy=[
    ['PERUNAT ',  5, 15],
    ['RIISI   ', 5, 15],
    ['EGG     ', 5, 0],
    ['VELLI   ', 5, 5],
    ['UUNIPERUNAT', 40, 0],
    ['LEIPA 200C', 20, 0],   
    ['TESTI', 1, 2]   
    ]

import tm1638,time
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))
direction=Pin(27,Pin.OUT)
step=Pin(26,Pin.OUT)
palohaly=Pin(15,Pin.IN)

tm.brightness(1)
UP=0
DOWN=1
SIJAINTI=0

def nosto(steps,suunta,speed=500):
    global SIJAINTI
    tm.brightness(7)
    direction.value(suunta)
    for x in range(steps):
        if suunta==UP: SIJAINTI+=1
        else: SIJAINTI-=1
        tm.number(SIJAINTI)
        tm.leds(x)
        step.value(1)
        time.sleep(1/speed)
        step.value(0)
        time.sleep(1/speed)
    time.sleep(1)
    tm.brightness(1)


def valinta(v):
    time.sleep(0.2)
    while True:
        tm.leds(2**v)
        tm.show('        ')
        if len(menyy[v][0])>8:
            tm.scroll(menyy[v][0],delay=100)
        tm.show(menyy[v][0][0:8])
        while True:
            k=tm.keys()
            if k>0:
                break
        time.sleep(1)
        if k==2**3:
            v=v+1
            if v==len(menyy):
                v=0
        if k==2**2:
            v=v-1
            if v<0:
                v=len(menyy)-1
        if k==2**7:
            break
    return v

def zfil(x):
    if x<10:
        return "  "+str(x)+" "
    elif x<100:
        return " "+str(x)+" "
    else:
        return " "+str(x)
    
def showtime (m1, m2):
    tm.show(zfil(m1)+zfil(m2))

def timerun(m1,m2,vasen):
    if vasen: minsaa=m1
    else: minsaa=m2
    mins=0
    while mins < minsaa:
        for y in range(6):
            for z in range(10):
                tm.led(y+1,1)
                if vasen: showtime(m1-mins,m2)
                else: showtime(m1,m2-mins)
                time.sleep(0.4)
                tm.led(7,1)
                tm.led(0,0)
                time.sleep(0.3)
                tm.led(7,0)
                tm.led(0,1)
                time.sleep(0.3)
                tm.leds(0)
                k=tm.keys()
                if k==2**7: return mins
                if k==2**0: mins+=1
                if k==2**1: mins-=1
                if mins==minsaa and z==9: return mins
                if palohaly.value()==0: return mins
        mins+=1
    return 0

TAPISSA=530
PUOLI=315

def taysi():
    nosto(TAPISSA-SIJAINTI,UP)

def puoli():
    nosto(TAPISSA-SIJAINTI,UP)
    nosto(TAPISSA-PUOLI-11,DOWN)
    nosto(11,DOWN,50)

def nolla():
    nosto(SIJAINTI-10,DOWN)
    
nosto(10,UP)

def keita(m1,m2):
    taysi()
    timerun(m1,m2,True)
    puoli()
    timerun(0,m2,False)
    nolla()

m1=1
m2=0
valo=1
while True:
    if palohaly.value()==0:
        tm.show('TULIPALO')
        time.sleep(10)
    time.sleep(0.1)
    k=tm.keys()
    tm.leds(2**valo)
    if k>0:
        valo=(valo+1)%8
        time.sleep(0.5)
    showtime(m1,m2)
    if k==2**0:
        m1=round(m1*1.5)
        if m1>500:
            m1=1
    if k==2**1:
        if m2==0:
            m2=1
        else:
            m2=round(m2*1.5)
        if m2>500:
            m2=0
    if k==2**2:
        v=valinta(0)
        m1=menyy[v][1]
        m2=menyy[v][2]
    if k==2**3:
        v=valinta(0)
        m1=menyy[v][1]
        m2=menyy[v][2]
    if k==2**7:
        keita(m1,m2)

