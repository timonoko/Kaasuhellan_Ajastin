
# Kaasukeittiön totaalinen haltuunotto (c) Tnoko 2023

import tm1638,time,machine
from machine import Pin

tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

palohaly=Pin(15,Pin.IN)

direction=Pin(27,Pin.OUT)
step=Pin(17,Pin.OUT)
stepable=Pin(5,Pin.OUT)

adc=machine.ADC(machine.Pin(33),atten=machine.ADC.ATTN_11DB)

def tempe1():
    return (adc.read()*2450/900)*100./4096-50.

TEMP=tempe1()

def tempera(): # Kohinainen lämpomittari, käytetään 10 otoksen keskiarvoa
    global TEMP
    TEMP=(99*TEMP+tempe1())/100
    return 24+int(TEMP)

tempera();tempera();tempera()

MIN_TEMP_ORIG=tempera()
if MIN_TEMP_ORIG>25: MIN_TEMP_ORIG=25
MIN_TEMP=MIN_TEMP_ORIG
MIN_TEMP_TIME=5
MAX_TEMP=50

tm.brightness(1)
UP=1
DOWN=0
SIJAINTI=0

def myscroll(x):
      tm.show('        ')
      if len(x)<9: tm.show(x)
      else:
        x='  '+x
        for i in range(0,len(x)-7):
             tm.show(x[i:(i+8)])
             time.sleep(0.2)

def kaasuhana(asento,speed=500):
    global SIJAINTI
    tm.brightness(7)
    steps=asento-SIJAINTI
    if steps==0: return
    if steps<0: suunta=DOWN
    else: suunta=UP
    print('steps,suunta=',steps,suunta)
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
#    time.sleep(1)
    tm.brightness(1)
    with open('SIJAINTI.TXT', 'w') as f:  f.write('%d' % SIJAINTI)

from MENYY import menyy

def valinta(v):
    time.sleep(0.2)
    while True:
        tm.leds(2**v)
        myscroll(menyy[v][0])
        while True:
            k=tm.keys()
            if k>0:
                break
        time.sleep(0.3)
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

def keys01(k):
    global aika1,aika2
    if k==2**0:
        if aika1==0:  aika1=1
        else: aika1=round(aika1*1.5)
        if aika1>500:  aika1=0
    if k==2**1:
        if aika2==0: aika2=1
        else: aika2=round(aika2*1.5)
        if aika2>500: aika2=0
    cou=0
    while tm.keys()>0:
        time.sleep(0.1)
        cou+=1
        if cou>3:
            if k==2**0: aika1=1
            if k==2**1: aika2=0

def hienosaato(k):  # Puoliliekin hienosäätö
    global PUOLI
    if k==2**5: PUOLI-=1
    else: PUOLI+=1
    puoli()
    tm.number(PUOLI)
    with open('PUOLI.TXT', 'w') as f:
        f.write('%d' % PUOLI)
    time.sleep(1)

def showtime (aika1, aika2):
    s=str(aika1)+" "+str(aika2)
    if MIN_TEMP==tempera(): s="E "+s
    elif MIN_TEMP>tempera(): s="- "+s
    while len(s)<6: s=" "+s
    tm.show(str(tempera())+s)

VIESTI=""
def keitto(kypalla): 
    global AIKA,MIN_TEMP_TIME,aika1,aika2,MIN_TEMP,VIESTI
    if kypalla: minsaa=aika1
    else: minsaa=aika2
    while minsaa > 0:
        for y in range(6):
            if y==4 and MIN_TEMP==100:  myscroll("SAMMUTA KATTILA")
            for z in range(10):
                tm.leds(0)
                tm.led(y+1,1)
                if kypalla: aika1=minsaa
                else: aika2=minsaa
                showtime(aika1,aika2)
                if palohaly.value()==0: aika2=0; VIESTI="TULIPALO"; return
                if tempera()>MAX_TEMP: aika2=0; VIESTI="YLILAMPO"; return 
                if AIKA>MIN_TEMP_TIME and tempera()<MIN_TEMP: aika2=0; VIESTI="ALILAMPO"; return
                for cnt in range(10):
                    time.sleep(0.1)
                    if cnt==0:   tm.led(7,1); tm.led(0,0)
                    elif cnt==3: tm.led(7,0); tm.led(0,1)
                    elif cnt==6: tm.led(7,0); tm.led(0,0)
                    k=tm.keys()
                    if k==2**0 or k==2**1:
                        keys01(k)
                        if kypalla: minsaa=aika1
                        else: minsaa=aika2
                    if k==2**5 or k==2**6: hienosaato(k)
                    if k==2**7: return
        minsaa-=1
        AIKA+=1
        print("AIKA,MIN_TEMP_TIME,MIN_TEMP,tempera()=",AIKA,MIN_TEMP_TIME,MIN_TEMP,tempera())
    return 0

TAPISSA=500
with open('PUOLI.TXT') as file: PUOLI = int(file.read())

def taysi():
    kaasuhana(TAPISSA)

def puoli():  # Puoliliekin kohtaa pitää lähestyä varoen ettei liekki sammu
    kaasuhana(PUOLI+100)
    kaasuhana(PUOLI,80)

def nolla():
    kaasuhana(-1) 

# Nostetaan hanaa ylös ja annetaan sen vapaasti pudota ==> Nollakohta

with open('SIJAINTI.TXT') as file:  SIJAINTI = int(file.read())
if SIJAINTI!=-1: SIJAINTI=30 # tähän asentoon se putoaa kun virta katkeaa
kaasuhana(0)
stepable.value(0) 
kaasuhana(100)
stepable.value(1)
kaasuhana(0)
stepable.value(0)
kaasuhana(-1) # naru löysälle, ettei veny

AIKA=0
def keita():
    global AIKA,MIN_TEMP_TIME,aika1,aika2,MIN_TEMP
    if aika1>10 and aika2==0: # Uunissa on oma liekinvarmistin
        tm.show('  UUNI  ')
        MIN_TEMP_TIME=aika1+1 # Loppuviesti "SAMMUTA KATTILA" jos sama
        MIN_TEMP=100
    else:
        tm.show(' KATTILA')
        MIN_TEMP_TIME=5
        MIN_TEMP=MIN_TEMP_ORIG
    while tm.keys()>0: pass
    if MIN_TEMP==100:
        while tm.keys()==0: myscroll("SAMMUTA KATTILA")
    AIKA=0
    taysi()
    keitto(kypalla=True)
    aika1=0
    if aika2==0:
        nolla()
        return
    puoli()
    keitto(kypalla=False)
    if aika1>0: keita() #uusiks
    aika2=0
    nolla()

aika1=2
aika2=0
valo=1

while True:
    time.sleep(0.1)
    k=tm.keys()
    tm.leds(2**valo)
    if k>0:
        valo=(valo+1)%8
        time.sleep(0.5)
    if VIESTI != "":
        tm.brightness(7)
        tm.show(VIESTI)
        time.sleep(1)
        tm.show("        ")
        time.sleep(1)
    else:
        showtime(aika1,aika2)
    if k==2**0 or k==2**1: # Keittoajat käsin
        keys01(k)
    if k==2**2 or k==2**3: # Keittoajat Menyystä
        v=valinta(0)
        aika1=menyy[v][1]
        aika2=menyy[v][2]
        keita() # Käynnistä Keittäminen Oitis
    if k==2**4:            # Kaasuhanan Testaus
        if SIJAINTI==TAPISSA: puoli()
        else: taysi()
    if k==2**5 or k==2**6: # Puoliliekin hienosäätö
        hienosaato(k)
    if k==2**7: # Käynnistä Keittäminen Oitis
        keita()

