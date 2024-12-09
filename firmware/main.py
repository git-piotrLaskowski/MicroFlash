import time
import machine
import servo

# Inicjalizacja serwa na pinie 23
servo = servo.Servo(pin=23, angle_max=180)

while True:
    print(f"Angle: 0-90")
    servo.smooth_move(0, 90, 2)
    print(servo.pwm.duty_ns())
    time.sleep(2)
    print(f"Angle: 90-160")
    servo.smooth_move(90, 160, 2)
    print(servo.pwm.duty_ns())
    time.sleep(2)
    print(f"Angle: 160-0")
    servo.smooth_move(160, 0, 3)
    print(servo.pwm.duty_ns())
    time.sleep(2)
