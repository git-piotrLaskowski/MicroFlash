import machine
import time


led = machine.Pin(2, machine.Pin.OUT)

while True:
    print("LED on")
    led.value(1)
    time.sleep(1)
    print("LED off")
    led.value(0)
    time.sleep(1)

