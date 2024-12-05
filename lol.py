import machine
import time

# Ustawienia PWM
pin_number = 13  # GPIO13
servo = machine.PWM(machine.Pin(pin_number), freq=50)  # Ustawiamy częstotliwość na 50 Hz

# Ustawienia wypełnienia dla serwa
min_duty = int((500 / 20000) * 1023)  # 500 µs dla 10-bitowego zakresu (1023 max)
max_duty = int((2500 / 20000) * 1023)  # 2500 µs dla 10-bitowego zakresu (1023 max)
mid_duty = (min_duty + max_duty) // 2

# Funkcja ustawiająca pozycję serwa
def set_servo_position(duty):
    servo.duty(duty)
    print(f"Servo set to duty {duty}")

try:
    while True:
        print("Servo: 0 degrees")
        set_servo_position(min_duty)
        time.sleep(2)

        print("Servo: 90 degrees")
        set_servo_position(mid_duty)
        time.sleep(2)

        print("Servo: 180 degrees")
        set_servo_position(max_duty)
        time.sleep(2)

except KeyboardInterrupt:
    print("Program interrupted by user")
    servo.deinit()

