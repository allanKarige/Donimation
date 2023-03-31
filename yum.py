from math import sin, cos, pi

DELTA_THETA = 0.07
DELTA_PHI = 0.02

R1 = 1
R2 = 2
K2 = 30

SCREEN_WIDTH = 36
SCREEN_HEIGHT = 36

K1 = SCREEN_WIDTH * K2 * 3 / (8 * (R1 + R2))

A0 = 1.0
DELTA_A = 0.08
B0 = 1.0
DELTA_B = 0.03

SYMBOLS = ".,-~:;=!*#$@"


def compute_frame(A, B):
    char_output = [[" " for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
    zbuffer = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    sinA, cosA = sin(A), cos(A)
    sinB, cosB = sin(B), cos(B)

    theta = 0
    while theta < 2 * pi:
        sintheta, costheta = sin(theta), cos(theta)
        theta += DELTA_THETA

        phi = 0
        while phi < 2 * pi:
            sinphi, cosphi = sin(phi), cos(phi)
            phi += DELTA_PHI

            circle_x, circle_y = R2 + R1 * costheta, R1 * sintheta

            x = (
                circle_x * (cosB * cosphi + sinA * sinB * sinphi)
                - circle_y * cosA * sinB
            )
            y = (
                circle_x * (sinB * cosphi - sinA * cosB * sinphi)
                + circle_y * cosA * cosB
            )
            z = K2 + cosA * circle_x * sinphi + circle_y * sinA
            ooz = 1 / z

            xp, yp = int(SCREEN_WIDTH / 2 + K1 * ooz * x), int(
                SCREEN_HEIGHT / 2 + K1 * ooz * y
            )

            luminance = (
                cosphi * costheta * sinB
                - cosA * costheta * sinphi
                - sinA * sintheta
                + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            )

            if luminance > 0 and ooz > zbuffer[xp][yp]:
                zbuffer[xp][yp] = ooz
                char_output[xp][yp] = SYMBOLS[int(luminance * 8)]

    return char_output


def frame_render(a, b):
    output = compute_frame(a, b)
    print("\x1b[H")
    for i in range(SCREEN_HEIGHT):
        for j in range(SCREEN_WIDTH):
            print(
                f"{output[i][j]}",
                end=""
            )
        print()


def donimation():
    a0, b0 = 0, 0
    while True:
        frame_render(a0, b0)
        a0 += DELTA_A
        b0 += DELTA_B


if __name__ == '__main__':
    donimation()

