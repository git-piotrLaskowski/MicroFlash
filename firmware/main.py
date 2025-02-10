import time
import math
import servo, machine

# Servo configuration
max_angle = 270
min_angle = 60
servo_0 = servo.Servo(pin=4, max_angle=max_angle, freq=50, min_us=500, max_us=2500)
servo_1 = servo.Servo(pin=5, max_angle=max_angle, freq=50, min_us=500, max_us=2500)
servo_2 = servo.Servo(pin=18, max_angle=max_angle, freq=50, min_us=500, max_us=2500)
led_0 = machine.Pin(21, machine.Pin.OUT)
led_1 = machine.Pin(22, machine.Pin.OUT)
pinMode = machine.Pin(23, machine.Pin.OUT)

def inverse_kinematics(coordinates):
    # Transform coordinates
    x = -1 * int(coordinates[0]) + 95
    y = -1 * int(coordinates[1]) + 85

    print(f"Transformed coordinates: ({x}, {y})")

    # Geometric parameters
    l1, l2 = 50, 90  # Lengths of the first and second arms (both sides are symmetrical)
    d = 40           # Distance between servo axes

    # Define workspace dynamically based on `y`
    if y > 85:
        workspace = {
            "min_x": 135,  # Expanded min_x if y < 0
            "max_x": -45,  # Expanded max_x if y < 0
            "min_y": 105,
            "max_y": 35
        }
    else:
        workspace = {
            "min_x": 95,  # Default min_x for y >= 0
            "max_x": -20, # Default max_x for y >= 0
            "min_y": 105,
            "max_y": 35
        }

    # Check if the point is within workspace boundaries
    if not (workspace["max_x"] <= x <= workspace["min_x"] and workspace["max_y"] <= y <= workspace["min_y"]):
        raise ValueError(f"Point ({x}, {y}) is outside the available working area.")

    # Calculate distance and angles for left and right arms
    def calculate_angles(a_x, a_y, l1, l2):
        dist = math.sqrt(a_x ** 2 + a_y ** 2)
        if dist == 0:
            raise ValueError(f"Coordinates ({a_x}, {a_y}) result in a distance of 0, leading to division by zero.")

        angle1 = math.acos(max(-1, min(1, (-l2 ** 2 + l1 ** 2 + dist ** 2) / (2 * l1 * dist))))
        angle2 = math.atan2(a_y, a_x)
        return angle1, angle2

    # Left arm calculations
    gamma, theta = calculate_angles(x, y, l1, l2)

    # Right arm calculations (adjust x-coordinate by `d`)
    epsilon, psi = calculate_angles(d - x, y, l1, l2)

    # Calculate servo angles in degrees
    q1 = math.degrees(theta + gamma)
    q2 = math.degrees(math.pi - epsilon - psi)

    return {
        "q1": q1,
        "q2": q2
    }

def click():
    try:
        servo_2.set_angle(30)
        time.sleep(0.2)
        servo_2.set_angle(0)
    except ValueError as e:
        print(f"Error: {e}")

def moveToXY(coordinates):
    try:
        angles = inverse_kinematics(coordinates)
        servo_0.set_angle(angles["q1"])
        servo_1.set_angle(90 + angles["q2"])
        time.sleep(0.0125)
        print(f"Calculated angles: {angles}")
    except ValueError as e:
        print(f"Error: {e}")


def moveBetweenPoints(point_0_coords, point_1_coords):
    x0, y0 = point_0_coords
    x1, y1 = point_1_coords

    dx = 1 if x0 < x1 else -1 if x0 > x1 else 0
    dy = 1 if y0 < y1 else -1 if y0 > y1 else 0

    x, y = x0, y0

    while x != x1 or y != y1:
        moveToXY((x, y))

        if x != x1:
            x += dx
        if y != y1:
            y += dy

    moveToXY((x1, y1))