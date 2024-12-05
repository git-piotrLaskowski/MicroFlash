import time
import adc_read
import servo


# Przykładowy pin (np. 34) do odczytu napięcia z potencjometru w serwomechanizmie
pin_number = 15

time.sleep(20)
servo.test_servo(0)   # Ustawienie na 0°
angle = adc_read.adc_read(pin_number)  # Wywołanie funkcji adc_read z podanym pinem
print(f"Servo arm angle: {angle:.2f}")  # Wyświetlenie wartości kąta
servo.test_servo(0)   # Ustawienie na 0°
time.sleep(1)
angle = adc_read.adc_read(pin_number)  # Wywołanie funkcji adc_read z podanym pinem
print(f"Servo arm angle: {angle:.2f}")  # Wyświetlenie wartości kąta
servo.test_servo(30)   # Ustawienie na 0°
time.sleep(1)
angle = adc_read.adc_read(pin_number)  # Wywołanie funkcji adc_read z podanym pinem
print(f"Servo arm angle: {angle:.2f}")  # Wyświetlenie wartości kąta
servo.test_servo(60)   # Ustawienie na 0°
time.sleep(1)
angle = adc_read.adc_read(pin_number)  # Wywołanie funkcji adc_read z podanym pinem
print(f"Servo arm angle: {angle:.2f}")  # Wyświetlenie wartości kąta
servo.test_servo(90)   # Ustawienie na 0°
time.sleep(1)
angle = adc_read.adc_read(pin_number)  # Wywołanie funkcji adc_read z podanym pinem
print(f"Servo arm angle: {angle:.2f}")  # Wyświetlenie wartości kąta
servo.test_servo(120)   # Ustawienie na 0°
time.sleep(1)
angle = adc_read.adc_read(pin_number)  # Wywołanie funkcji adc_read z podanym pinem
print(f"Servo arm angle: {angle:.2f}")  # Wyświetlenie wartości kąta
servo.test_servo(150)   # Ustawienie na 0°
time.sleep(1)
angle = adc_read.adc_read(pin_number)  # Wywołanie funkcji adc_read z podanym pinem
print(f"Servo arm angle: {angle:.2f}")  # Wyświetlenie wartości kąta
servo.test_servo(180)   # Ustawienie na 0°
time.sleep(1)