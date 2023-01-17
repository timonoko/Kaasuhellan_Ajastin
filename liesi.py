
import tm1638,time,machine
from machine import Pin

tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

palohaly=Pin(15,Pin.IN)

direction=Pin(27,Pin.OUT)
step=Pin(17,Pin.OUT)
stepable=Pin(5,Pin.OUT)

adc=machine.ADC(machine.Pin(33),atten=machine.ADC.ATTN_11DB)

MAX_TEMP=70
MIN_TEMP=30

def tempe1():
    return (adc.read()*2450/900)*100./4096-50.

TEMP=tempe1()

def tempera():
    global TEMP
    TEMP=(9*TEMP+tempe1())/10
    return 24+int(TEMP)

tm.brightness(1)
UP=1
DOWN=0
SIJAINTI=0

def kaasuhana(asento,speed=500):
    global SIJAINTI
    tm.brightness(7)
    steps=asento-SIJAINTI
    if steps==0: return
    if steps<0: suunta=DOWN
    else: suunta=UP
    print('sd=',steps,suunta)
    direction.value(suunta)
    for x in range(abs(steps)):
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

from MENYY import menyy

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


def showtime (m1, m2):
    s=str(m1)+" "+str(m2)
    while len(s)<6: s=" "+s
    tm.show(str(tempera())+s)

def timerun(m1,m2,vasen):
    global AIKA
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
                if tempera()>MAX_TEMP: return mins
                if AIKA>3 and tempera()<MIN_TEMP: return mins
        mins+=1
        AIKA+=1
        print("AIKA=",AIKA)
    return 0

TAPISSA=530
with open('PUOLI.TXT') as file:
     PUOLI = int(file.read())

def taysi():
    kaasuhana(TAPISSA)

def puoli():
    kaasuhana(PUOLI+100)
    kaasuhana(PUOLI,80)

def nolla():
    kaasuhana(0)

stepable.value(0)
kaasuhana(30)
stepable.value(1)
nolla()
stepable.value(0)

AIKA=0
def keita(m1,m2):
    global AIKA
    AIKA=0
    taysi()
    timerun(m1,m2,True)
    if m2==0:
        nolla()
        return
    puoli()
    timerun(0,m2,False)
    nolla()

showtime(MIN_TEMP,MAX_TEMP)
time.sleep(1)

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
    if k==2**4:
        if SIJAINTI==TAPISSA: puoli()
        elif SIJAINTI==PUOLI: nolla()
        else: taysi()
    if k==2**5:
        PUOLI-=1
        puoli()
        tm.number(PUOLI)
        with open('PUOLI.TXT', 'w') as f: f.write('%d' % PUOLI)
        time.sleep(1)
    if k==2**6:
        PUOLI+=1
        puoli()
        tm.number(PUOLI)
        with open('PUOLI.TXT', 'w') as f: f.write('%d' % PUOLI)
        time.sleep(1)
    if k==2**7:
        keita(m1,m2)

