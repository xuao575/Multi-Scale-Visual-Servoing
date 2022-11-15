from sift.sift import sift
import numpy as np
from sympy import symbols, Eq, solve


def calc(img1, img2, dist):
    x_norm1 = calc_two_pic(img1, img2)
    # x_norm2 = -calc_two_pic(img1, img3)

    # get working distance from micro lens
    working_dist = 16.9

    # x, y = symbols('x y')
    # eq1 = Eq(x * (dist / working_dist) + y - x_norm1, 0)
    # eq2 = Eq(x * (-dist / working_dist) + y - x_norm2, 0)
    # sol = solve((eq1, eq2), (x, y))
    # print(sol)


    # fx =
    # fy
    # cx
    # cy
    print(x_norm1 * working_dist / dist)

    intrinsic = np.array([[], [], []])
    return intrinsic


def calc_two_pic(img1, img2, num=10):
    pts1, pts2 = sift(img1, img2, num)
    d_pts = pts1 - pts2

    # mean first
    x_mean = d_pts[:, 0].mean()
    y_mean = d_pts[:, 1].mean()
    norm = np.linalg.norm([x_mean, y_mean], axis=0)
    return norm
