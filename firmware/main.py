import time
import machine
import servo
import json

# Initialize servos
servos = [
    servo.Servo(pin=12),  # Base servo
    servo.Servo(pin=11),  # Arm servo 1
    servo.Servo(pin=14),  # Arm servo 2
    servo.Servo(pin=15),  # Gripper servo
]

# Initialize angles for each servo
angles = [90, 90, 90, 90]
current_servo = 0

# Initialize buttons
upperButton = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)
lowerButton = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_DOWN)
nextButton = machine.Pin(42, machine.Pin.IN, machine.Pin.PULL_DOWN)
prevButton = machine.Pin(41, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Debounce time in seconds
debounce_time = 0.025  # This is used for the upperButton and lowerButton
save_hold_time = 1  # Time in seconds to hold the button for saving

# File to store servo positions
position_file = "positions.json"
current_package = []  # Temporary storage for the current "package" of positions
all_packages = []  # All completed "packages"

# Load saved packages if file exists
try:
    with open(position_file, "r") as file:
        all_packages = json.load(file)
        print("Loaded saved packages:", all_packages)
except OSError:
    print("No saved packages found, starting fresh.")

# Initialize RGB LED (connected to pins 13, 14, 15 for example)
rgb_led = machine.Pin(13, machine.Pin.OUT)
green_led = machine.Pin(14, machine.Pin.OUT)
blue_led = machine.Pin(15, machine.Pin.OUT)


def signal_package_saved():
    """Blink the RGB LED green when a package is saved."""
    for _ in range(3):  # Blink 3 times
        green_led.value(1)
        time.sleep(0.2)
        green_led.value(0)
        time.sleep(0.2)


# Button states and timers for detecting long press
prev_next_state = 0
next_button_hold_start = None
prev_button_hold_start = None

# Main loop
while True:
    # Select the current servo
    servo = servos[current_servo]

    # Check upper button for increasing angle
    if upperButton.value():  # Button pressed (high state)
        angles[current_servo] = min(180, angles[current_servo] + 1)  # Increase angle
        servo.set_angle(angles[current_servo])
        print(f"Servo {current_servo} Angle: {angles[current_servo]}")
        time.sleep(debounce_time)

    # Check lower button for decreasing angle
    if lowerButton.value():  # Button pressed (high state)
        angles[current_servo] = max(0, angles[current_servo] - 1)  # Decrease angle
        servo.set_angle(angles[current_servo])
        print(f"Servo {current_servo} Angle: {angles[current_servo]}")
        time.sleep(debounce_time)

    # Detect long press for nextButton
    current_next_state = nextButton.value()
    if current_next_state and not prev_next_state:  # Rising edge detected
        next_button_hold_start = time.time()
    elif not current_next_state and prev_next_state:  # Falling edge detected
        if next_button_hold_start and time.time() - next_button_hold_start >= save_hold_time:
            # Add current servo angles to the package
            current_package.append(angles[current_servo])
            print(f"Added angle {angles[current_servo]} for Servo {current_servo} to the package.")

            # Check if package is complete (4 positions)
            if len(current_package) == 4:
                all_packages.append(current_package)  # Add package to list
                current_package = []  # Clear temporary package
                print("Package completed and saved:", all_packages[-1])

                # Save to file
                with open(position_file, "w") as file:
                    json.dump(all_packages, file)
                print("All packages saved to file.")

                # Signal that the package has been saved
                signal_package_saved()

            # Switch to the next servo
            current_servo = (current_servo + 1) % len(servos)
            print(f"Switched to Servo {current_servo}")

        next_button_hold_start = None  # Reset timer after button is released
    prev_next_state = current_next_state

    # Detect long press for prevButton
    current_prev_state = prevButton.value()
    if current_prev_state and not prev_next_state:  # Rising edge detected
        prev_button_hold_start = time.time()
    elif not current_prev_state and prev_next_state:  # Falling edge detected
        if prev_button_hold_start and time.time() - prev_button_hold_start >= save_hold_time:
            # Remove last added angle for the previous servo
            if current_package:
                removed_angle = current_package.pop()
                print(f"Removed angle {removed_angle} for Servo {current_servo}")

            # Switch to the previous servo
            current_servo = (current_servo - 1) % len(servos)
            print(f"Switched to Servo {current_servo}")

        prev_button_hold_start = None  # Reset timer after button is released
    prev_next_state = current_prev_state
