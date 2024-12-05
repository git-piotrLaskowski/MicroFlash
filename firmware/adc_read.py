import machine

# Funkcja odczytująca wartość z ADC i przeliczająca ją na kąt
def adc_read(adc_pin):
    # Inicjalizacja ADC
    adc = machine.ADC(machine.Pin(adc_pin))  # Inicjalizacja ADC na wskazanym pinie
    adc.atten(machine.ADC.ATTN_0DB)  # Ustawienie zakresu napięcia od 0V do 3.3V

    # Odczyt wartości z ADC (od 0 do 4095)
    raw_value = adc.read()

    # Przekształcenie wartości ADC na kąt (0-180)
    angle = (raw_value / 4095) * 180  # Przekształcenie na zakres 0-180°


    return angle

