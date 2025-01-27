import math

def inverse_kinematics(coordinates):
    x = coordinates[0]
    y = coordinates[1]

    l1l, l1r = 50, 50
    l2l, l2r = 90, 90
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

    return  c, e, gamma, theta, epsilon, psi, q1, q2


coords = (20, 50)
print(f"c: {inverse_kinematics(coords)[0]}, "
    f"\ne: {inverse_kinematics(coords)[1]}, "
    f"\ngamma: {math.degrees(inverse_kinematics(coords)[2])}, "
    f"\ntheta: {math.degrees(inverse_kinematics(coords)[3])}, "
    f"\nepsilon: {math.degrees(inverse_kinematics(coords)[4])}, "
    f"\npsi: {math.degrees(inverse_kinematics(coords)[5])},       "
    f"\nq1: {inverse_kinematics(coords)[6]},       "
    f"\nq2: {inverse_kinematics(coords)[7]}")
