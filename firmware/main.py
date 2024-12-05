import machine
import time


class Servo:
    def __init__(self, pin_number, freq=50, min_us=500, max_us=2500, range_bits=10):
        """
        Klasa do sterowania serwomechanizmami za pomocą PWM.

        :param pin_number: Numer pinu GPIO podłączonego do serwa.
        :param freq: Częstotliwość PWM w Hz (domyślnie 50 Hz dla serwomechanizmów).
        :param min_us: Minimalny czas impulsu w mikrosekundach (domyślnie 500 µs).
        :param max_us: Maksymalny czas impulsu w mikrosekundach (domyślnie 2500 µs).
        :param range_bits: Rozdzielczość PWM w bitach (domyślnie 10 bitów = 1023 max).
        """
        self.pin_number = pin_number
        self.freq = freq
        self.min_duty = int((min_us / 20000) * (2 ** range_bits - 1))
        self.max_duty = int((max_us / 20000) * (2 ** range_bits - 1))
        self.range_bits = range_bits

        # Inicjalizacja PWM
        self.pwm = machine.PWM(machine.Pin(pin_number), freq=freq)
        self.current_duty = (self.min_duty + self.max_duty) // 2  # Środek zakresu

    def set_angle(self, angle):
        """
        Ustawia kąt serwa (od 0 do 180 stopni).

        :param angle: Kąt serwa (0-180 stopni).
        """
        if not 0 <= angle <= 180:
            raise ValueError("Kąt musi być w zakresie od 0 do 180 stopni.")

        # Przeliczanie kąta na wartość PWM
        duty = self.min_duty + int((angle / 180) * (self.max_duty - self.min_duty))
        self.pwm.duty(duty)
        self.current_duty = duty

    def smooth_move(self, target_angle, duration_ms=1000, step_delay_ms=20):
        """
        Wykonuje płynny ruch serwa do docelowego kąta.

        :param target_angle: Docelowy kąt serwa (0-180 stopni).
        :param duration_ms: Czas trwania ruchu w milisekundach.
        :param step_delay_ms: Opóźnienie między krokami w milisekundach.
        """
        if not 0 <= target_angle <= 180:
            raise ValueError("Kąt musi być w zakresie od 0 do 180 stopni.")

        # Obliczenie liczby kroków
        steps = duration_ms // step_delay_ms
        start_angle = (self.current_duty - self.min_duty) / (self.max_duty - self.min_duty) * 180
        step_size = (target_angle - start_angle) / steps

        for i in range(steps):
            current_angle = start_angle + step_size * (i + 1)
            self.set_angle(current_angle)
            time.sleep_ms(int(step_delay_ms))

    def deinit(self):
        """Wyłącza PWM dla serwa."""
        self.pwm.deinit()


def runArm():
    # Inicjalizacja serwa
    servo1 = Servo(pin_number=13)  # Serwo na pinie GPIO13
    try:
        while True:
            # Ruch do 0 stopni
            print("Ruch do 20 stopni")
            servo1.smooth_move(20, duration_ms=1500)
            time.sleep(2)

            # Płynny ruch do 90 stopni
            print("Ruch do 90 stopni")
            servo1.smooth_move(90, duration_ms=1500)
            time.sleep(2)

            # Ruch do 180 stopni
            print("Ruch do 110 stopni")
            servo1.smooth_move(110, duration_ms=1500)
            time.sleep(2)

    except KeyboardInterrupt:
        print("Przerwano działanie programu.")
    finally:
        servo1.deinit()

if __name__ == "__main__":
    runArm()