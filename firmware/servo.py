import machine
import time

# Konfiguracja pinu PWM
servo = machine.PWM(machine.Pin(23), freq=50)  # Pin 2, częstotliwość 50 Hz

# Funkcja ustawiająca kąt serwa
def set_angle(angle):
    # Zmiana szerokości impulsu, odpowiednia do kąta
    # Zakładając, że kąt 0° to 1ms, a kąt 270° to 2ms.
    # Przekształcamy kąt na szerokość impulsu (zakres 1 ms do 2 ms)
    pulse_width = int(0 + (angle / 180) * 180)
    print(pulse_width)
    servo.duty(pulse_width)

# Funkcja do testowego ustawiania kątów w `servo.py`
def test_servo(angle):
    set_angle(angle)
    time.sleep(1)
