import machine
import time
import math

class Servo:
    def __init__(self, pin, angle_max=180, freq=50, min_us=500, max_us=2000, res=16):
        self.pin_number = pin
        self.freq = freq
        self.angle_max = angle_max
        self.min_us = min_us
        self.max_us = max_us
        self.res = res

        # Calculate minimum and maximum duty cycle values based on pulse width
        self.min_duty = int((min_us / (1_000_000 / freq)) * (2 ** res - 1))
        self.max_duty = int((max_us / (1_000_000 / freq)) * (2 ** res - 1))

        # Initialize PWM
        self.pwm = machine.PWM(machine.Pin(pin))
        self.pwm.freq(freq)

    def set_angle(self, angle):
        """
        Sets the servo to the specified angle with better precision for small angles.
        :param angle: Target angle in degrees (must be between 0 and 180).
        """
        if not 0 <= angle <= self.angle_max:
            raise ValueError(f"Angle must be between 0 and {self.angle_max} degrees.")

        # Apply a logarithmic or smooth mapping to get better precision for small angles
        # The formula below uses a more gradual scaling for smaller angles.
        # duty = (angle / self.angle_max) * (self.max_duty - self.min_duty) + self.min_duty

        # For more precise control over small angles, use exponential scaling:
        duty = int(self.min_duty + (self.max_duty - self.min_duty) * (1 - math.exp(-angle / 50.0)))

        # Apply the duty cycle to the servo
        self.pwm.duty_u16(duty)

    def smooth_move(self, start_angle, end_angle, duration, steps=50):
        step_time = duration / steps
        for step in range(steps + 1):
            # Linear interpolation for angle
            angle = start_angle + (end_angle - start_angle) * (step / steps)
            self.set_angle(angle)
            time.sleep(step_time)

    def deinit(self):
        self.pwm.deinit()
