import time
import servo

servo = servo.Servo(pin=23)

angle = 0
servo.set_angle(angle)   # Ustawienie na 0°
for angle in range(0, 180, 10):
    print(f"Servo arm angle: {angle:.2f}")  # Wyświetlenie wartości kąta
    servo.set_angle(angle)   # Ustawienie na 0°
    #angle+=10
    time.sleep(0.5)
