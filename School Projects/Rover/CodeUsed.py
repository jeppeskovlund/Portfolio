# -*- coding: utf-8 -*-
from socket import *
from time import sleep

import RPi.GPIO as G

MIN_STOP = 47
MAX_STOP = 53
print("Kører serveren\n")

# host = "192.168.1.215" # Min PC
host = "192.168.1.107"  # Dette er IP-adressen for Raspberry Pi
port = 3000  # Husk at portnumre på 1024 og lavere er priviligerede
porty = 4000
s = socket(AF_INET, SOCK_DGRAM)
s.bind((host, port))  # Binds the socket. Note that the input to
k = socket(AF_INET, SOCK_DGRAM)
k.bind((host, porty))

G.setmode(G.BCM)
motorM1, motorM2, motorM3, motorM4 = 20, 16, 26, 21
G.setup([motorM1, motorM2, motorM3, motorM4], G.OUT)
m1, m2, m3, m4 = G.PWM(motorM1, 100), G.PWM(
    motorM2, 100), G.PWM(motorM3, 100), G.PWM(motorM4, 100)
m1.start(0)  # fremad højre
m2.start(0)  # baglæns højre
m3.start(0)  # fremad venstre
m4.start(0)  # baglæns højre


def forward(y):
    m1.ChangeDutyCycle(y)
    m2.ChangeDutyCycle(0)
    m3.ChangeDutyCycle(y)
    m4.ChangeDutyCycle(0)


def forward_right(x, y):
    m1.ChangeDutyCycle(y)
    m2.ChangeDutyCycle(0)
    m3.ChangeDutyCycle(100*(1-x/100))
    m4.ChangeDutyCycle(0)


def forward_left(x, y):
    m1.ChangeDutyCycle(x)
    m2.ChangeDutyCycle(0)
    m3.ChangeDutyCycle(y)
    m4.ChangeDutyCycle(0)


def backward(y):
    m1.ChangeDutyCycle(0)
    m2.ChangeDutyCycle(100*(1-y/100))
    m3.ChangeDutyCycle(0)
    m4.ChangeDutyCycle(100*(1-y/100))


def backward_right(x, y):
    m1.ChangeDutyCycle(0)
    m2.ChangeDutyCycle((100*(1-y/100)))
    m3.ChangeDutyCycle(0)
    m4.ChangeDutyCycle(100*(1-x/100))


def backward_left(x, y):
    m1.ChangeDutyCycle(0)
    m2.ChangeDutyCycle(100*(1-x/100))
    m3.ChangeDutyCycle(0)
    m4.ChangeDutyCycle(100*(1-y/100))


def left(x):
    m1.ChangeDutyCycle(x)
    m2.ChangeDutyCycle(0)
    m3.ChangeDutyCycle(100*(1-x/100))
    m4.ChangeDutyCycle(0)


def right(x):
    m1.ChangeDutyCycle(x)
    m2.ChangeDutyCycle(0)
    m3.ChangeDutyCycle(100-x)
    m4.ChangeDutyCycle(0)


def stop():
    m1.ChangeDutyCycle(0)
    m2.ChangeDutyCycle(0)
    m3.ChangeDutyCycle(0)
    m4.ChangeDutyCycle(0)


while True:
    sleep(0.1)
    l, addr = s.recvfrom(1024)
    x = int(l)
    # print( "x:" + x.strip().decode('utf-8'))

    p, addr = k.recvfrom(1024)
    y = int(p)
   # print( "y:" + y.strip().decode('utf-8'))

    if y >= MAX_STOP and x >= MAX_STOP:
        forward_right(x, y)
        print("Forward Right")
    elif y >= MAX_STOP and x <= MIN_STOP:
        forward_left(x, y)
        print("Forward Left")
    elif y >= MAX_STOP and x >= MIN_STOP and x <= MAX_STOP:
        print("Forward")
        forward(y)
    elif y <= MIN_STOP and x >= MAX_STOP:
        backward_right(x, y)
        print("Backward Right")
    elif y <= MIN_STOP and x <= MIN_STOP:
        backward_left(x, y)
        print("Backward Left")
    elif y <= MIN_STOP and x >= MIN_STOP and x <= MAX_STOP:
        print("Backward")
        backward(y)
    elif x <= MIN_STOP:
        left(x)
        print("Left")
    elif x >= MAX_STOP:
        right(x)
        print("Right")
    else:
        print("Stop")
        stop()
skt.close()
G.cleanup

"""
    if move == "w":
        print("W - Fremad")
        m1.ChangeDutyCycle(0)
        m2.ChangeDutyCycle(100)
        m3.ChangeDutyCycle(0)
        m4.ChangeDutyCycle(100)

    elif move == "s":
        print("S - Tilbage")
        m1.ChangeDutyCycle(100)
        m2.ChangeDutyCycle(0)
        m3.ChangeDutyCycle(100)
        m4.ChangeDutyCycle(0)

    elif move == "d":
        print("D - Højre")
        m1.ChangeDutyCycle(0)
        m2.ChangeDutyCycle(50)
        m3.ChangeDutyCycle(0)
        m4.ChangeDutyCycle(100)

    elif move == "a":
        print("A - Venstre")
        m1.ChangeDutyCycle(0)
        m2.ChangeDutyCycle(100)
        m3.ChangeDutyCycle(0)
        m4.ChangeDutyCycle(50)

    elif move == "stop":
        print("Stop")
        m1.ChangeDutyCycle(0)
        m2.ChangeDutyCycle(0)
        m3.ChangeDutyCycle(0)
        m4.ChangeDutyCycle(0)

    elif move == "q":
        print("Q - Neutral")
        m1.ChangeDutyCycle(0)
        m2.ChangeDutyCycle(0)
        m3.ChangeDutyCycle(0)
        m4.ChangeDutyCycle(0)
        elif move == "r":
        skt.close()
        G.cleanup
        exit
"""
