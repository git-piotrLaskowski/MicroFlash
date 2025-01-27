import machine
import time, math

class Servo:
    """Class for controlling servo motors via PWM."""

    def __init__(self, pin, max_angle=180, freq=50, min_us=500, max_us=2500, res=16):
        self.pin_number = pin
        self.freq = freq
        self.max_angle = max_angle
        self.min_us = min_us
        self.max_us = max_us
        self.range_bits = res
        self.period_us = int(1_000_000 / freq)
        self.current_angle = max_angle // 2

        self.min_duty = self.calculate_duty(min_us)
        self.max_duty = self.calculate_duty(max_us)

        self.allowed_interpolations = {"sin", "lin", "cub", "quad"}

        if not (0 < min_us < max_us):
            raise ValueError("min_us must be less than max_us and both must be positive.")
        if not (8 <= res <= 16):
            raise ValueError("Resolution must be between 8 and 16 bits.")

        try:
            self.pwm = machine.PWM(machine.Pin(pin), freq=freq)
            self.set_angle(self.current_angle)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize PWM on pin {pin}: {e}")

    def __del__(self):
        """Ensures PWM is turned off when the object is deleted."""
        self.deinit()

    def calculate_duty(self, pulse_us):
        """Converts pulse width in microseconds to duty cycle value."""
        duty = (pulse_us * (2 ** self.range_bits - 1)) // self.period_us
        return int(duty)

    def set_angle(self, angle):
        """Sets the servo angle."""
        if not (0 <= angle <= self.max_angle):
            raise ValueError(f"Angle must be between 0 and {self.max_angle}.")
        self.current_angle = angle
        # Interpolate pulse width for the given angle
        pulse_us = self.min_us + (self.max_us - self.min_us) * angle // self.max_angle
        duty = self.calculate_duty(pulse_us)
        self.pwm.duty_u16(duty)

    def smooth_move(self, start_angle, end_angle, duration, steps=None, interpolation="sin"):
        """Moves the servo smoothly from start_angle to end_angle."""
        if steps is None:
            step_time = 0.02
            steps = int(duration / step_time)
        else:
            step_time = duration / steps

        if interpolation not in self.allowed_interpolations:
            raise ValueError(f"Unsupported interpolation method. Choose from {self.allowed_interpolations}.")

        delta_angle = end_angle - start_angle
        for step in range(steps + 1):
            t = step / steps
            if interpolation == "sin":
                t = 0.5 - 0.5 * math.cos(math.pi * t)
            elif interpolation == "lin":
                pass  # t = t by default
            elif interpolation == "cub":
                t = 3 * t ** 2 - 2 * t ** 3
            elif interpolation == "quad":
                t = t ** 2
            angle = start_angle + delta_angle * t
            self.set_angle(angle)
            time.sleep(step_time)

    def center(self):
        """Resets the servo to its center position."""
        self.set_angle(self.max_angle // 2)

    def disable(self, stop_pwm=False):
        """Disables the PWM signal. Optionally stops PWM."""
        self.pwm.duty_u16(0)
        if stop_pwm:
            self.pwm.deinit()

    def deinit(self):
        """Deinitializes the servo by turning off the PWM."""
        self.pwm.deinit()

    @property
    def angle(self):
        """Returns the current angle of the servo."""
        return self.current_angle

    @angle.setter
    def angle(self, value):
        """Sets the angle of the servo."""
        self.set_angle(value)