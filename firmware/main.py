import time
import machine
import servo

# Initialize two servos on GPIO12 and GPIO13
servos = [servo.Servo(pin=12), servo.Servo(pin=11)]

# Initial angles for each servo
angles = [90, 90]
current_servo = 0

# Initialize buttons
upperButton = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)
lowerButton = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_DOWN)
nextButton = machine.Pin(42, machine.Pin.IN, machine.Pin.PULL_DOWN)
prevButton = machine.Pin(41, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Debounce time in seconds
debounce_time = 0.025

# Button states for edge detection
prev_next_state = 0
prev_prev_state = 0

# Main loop
while True:
    # Select the current servo
    servo = servos[current_servo]

    # Check upper button for increasing angle
    if upperButton.value():  # Button pressed (high state)
        angles[current_servo] = min(160, angles[current_servo] + 1)  # Increase angle
        servo.set_angle(angles[current_servo])
        print(f"Servo {current_servo} Angle: {angles[current_servo]}")
        time.sleep(debounce_time)

    # Check lower button for decreasing angle
    if lowerButton.value():  # Button pressed (high state)
        angles[current_servo] = max(0, angles[current_servo] - 1)  # Decrease angle
        servo.set_angle(angles[current_servo])
        print(f"Servo {current_servo} Angle: {angles[current_servo]}")
        time.sleep(debounce_time)

    # Detect rising edge for nextButton
    current_next_state = nextButton.value()
    if current_next_state and not prev_next_state:  # Rising edge detected
        current_servo = (current_servo + 1) % len(servos)  # Move to the next servo
        print(f"Switched to Servo {current_servo}")
        time.sleep(debounce_time)
    prev_next_state = current_next_state

    # Detect rising edge for prevButton
    current_prev_state = prevButton.value()
    if current_prev_state and not prev_prev_state:  # Rising edge detected
        current_servo = (current_servo - 1) % len(servos)  # Move to the previous servo
        print(f"Switched to Servo {current_servo}")
        time.sleep(debounce_time)
    prev_prev_state = current_prev_state
