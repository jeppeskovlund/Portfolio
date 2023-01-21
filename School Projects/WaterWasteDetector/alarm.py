import os
from time import sleep

import RPi.GPIO as G

LIMIT = 48

G.setmode(G.BCM)
LED_RED = 24
BUZZER = 27
G.setup([LED_RED, BUZZER], G.OUT)
buz = G.PWM(BUZZER, 1000)
BUTTON = 17
G.setup(BUTTON, G.IN)
G.add_event_detect(BUTTON, G.RISING, bouncetime=200)

file_count = "calibration/count"

if os.path.exists(file_count):
    with open(file_count) as f:
        count = int(f.read())
else:
    count = 0


if count > LIMIT:
    while True:
        buz.start(80)
        G.output(LED_RED, G.HIGH)
        sleep(1.5)
        buz.stop()
        G.output(LED_RED, G.LOW)
        sleep(0.5)
        if G.event_detected(BUTTON):
            print("pressed")
            with open(file_count, "w") as f:
                f.write("0")
            break

G.cleanup()
