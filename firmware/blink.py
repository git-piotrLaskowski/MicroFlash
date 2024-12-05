import machine
import time

# Konfiguracja pinu GPIO2 jako wyjścia
led = machine.Pin(2, machine.Pin.OUT)

# Funkcja mrugania diodą
def blink(led, delay=0.5):
    while True:
        print("LED on")
        led.on()  # Włącz diodę
        time.sleep(delay)  # Odczekaj
        print("LED off")
        led.off()  # Wyłącz diodę
        time.sleep(delay)  # Odczekaj
