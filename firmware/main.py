import time
import math
import servo

max_angle = 270
min_angle = 60
servo_0 = servo.Servo(pin=2, max_angle=max_angle, freq=50, min_us=500, max_us=2500)
servo_1 = servo.Servo(pin=4, max_angle=max_angle, freq=50, min_us=500, max_us=2500)


def inverse_kinematics(coordinates):
    x = int(coordinates[0])
    y = int(coordinates[1])

    l1l, l1r = 50, 50
    l2l, l2r = 90, 90
    d = 40

    """Calculating angles for left side of arm"""
    c = math.sqrt(x ** 2 + y ** 2)
    if c == 0:
        raise ValueError("Coordinates cannot be (0, 0) because it leads to division by zero.")

    gamma = math.acos(max(-1, min(1, (- l2l ** 2 + l1l ** 2 + c ** 2) / (2 * l1l * c))))  # Clamp to avoid domain errors
    theta = math.atan2(y, x)  # atan2 handles x=0 safely
    q1 = math.degrees(theta + gamma)

    """Calculating angles for right side of arm"""
    e = math.sqrt((d - x) ** 2 + y ** 2)
    if e == 0:
        raise ValueError(f"Coordinates ({x}, {y}) result in e=0, which leads to division by zero.")

    epsilon = math.acos(
        max(-1, min(1, (- l2r ** 2 + l1r ** 2 + e ** 2) / (2 * l1r * e))))  # Clamp to avoid domain errors
    psi = math.atan2(y, d - x)  # atan2 handles (d - x) = 0 safely
    q2 = math.degrees(math.pi - epsilon - psi)

    return gamma, theta, epsilon, psi, q1, q2

def moveToXY(coords):
    servo_0.set_angle(-90 + inverse_kinematics(coords)[4])
    servo_1.set_angle(90 + inverse_kinematics(coords)[5])
    time.sleep(0.025)


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

