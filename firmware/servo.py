import machine
import time

class Servo:
    def __init__(self, pin, freq=50):
        """
        Servo initialization
        :param pin: Number of pin GPIO connected to the servo
        :param freq: PWM frequency (default 50Hz for standard servos
        """
        self.pin = machine.Pin(pin)
        self.pwm = machine.PWM(self.pin)
        self.pwm.freq(freq)
        self.min_duty = 1024 # Minimum duty cycle for ~1 ms
        self.max_duty = 8192 # Maximum duty cycle for ~2 ms
        self.set_angle(90)   # Set servo in neutral position (90 degrees)

    def set_angle(self, angle):
        """
        Sets angle of servo
        :param angle: Angle in degrees (0-180)
        """
        if not 0 <= angle <= 180:
            raise ValueError("Angle has to be between 0-180 degrees. ")

        duty = int(self.min_duty + (self.max_duty - self.min_duty) * (angle/180))
        self.pwm.duty_u16(duty)

    def deinit(self):
        """
        Deinitialization of servo by turning off the PWM
        """
        self.pwm.deinit()