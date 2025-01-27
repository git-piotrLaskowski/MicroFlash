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

    l1l = 50
    l1r = 50
    l2l = 90
    l2r = 90
    d = 40

    """Calculating angles for left side of arm"""
    c = math.sqrt(x ** 2 + y ** 2)
    gamma = math.acos((- l2l**2 + l1l**2 + c**2) / (2 * l1l * c))
    theta = math.atan(y / x)
    q1 = math.degrees(theta + gamma)

    """Calculating angles for right side of arm"""
    e = math.sqrt((d - x) ** 2 + y ** 2)
    epsilon  = math.acos((- l2r**2 + l1r**2 + e**2) / (2 * l1r * e))
    psi = math.atan(y / (d - x))
    q2 = math.degrees(math.pi - epsilon - psi)

    return  gamma, theta, epsilon, psi, q1, q2


coords = (1, 90)
print(f"gamma: {inverse_kinematics(coords)[0]}, "
      f"\ntheta: {inverse_kinematics(coords)[1]}, "
      f"\nepsilon: {inverse_kinematics(coords)[2]}, "
      f"\npsi: {inverse_kinematics(coords)[3]},       "
      f"\nq1: {inverse_kinematics(coords)[4]},       "
      f"\nq2: {inverse_kinematics(coords)[5]}")


angle_0 = -90 + inverse_kinematics(coords)[4]
print(angle_0)
servo_0.set_angle(angle_0)
time.sleep(1)
angle_1 = 90 + inverse_kinematics(coords)[5]
print(angle_1)
servo_1.set_angle(angle_1)
time.sleep(1)

#servo_0.deinit()
#servo_1.deinit()


