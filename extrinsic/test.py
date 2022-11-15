import numpy as np

from pi_init import pi_init, get_pose, mov
from autofocus import AutoFocus, VideoCapture, waiting
from sift.sift import sift
import time
import cv2


def main():
    # init
    pidevice = pi_init()
    vid = VideoCapture()
    waiting(vid)

    # focus
    af = AutoFocus(10)
    target_z = af.autofocus_simple(pidevice, vid)
    mov(pidevice, [0, 0, target_z, 0, 0, 0])

    extrinsic_x_origin = 125
    extrinsic_y_origin = 0
    extrinsic_z_origin = 0

    _range = 5
    func_map = np.zeros([_range, _range])
    for i in range(_range):
        for j in range(_range):
            # 0.1 mm
            extrinsic_x = extrinsic_x_origin + ((i - _range // 2) / 10)
            extrinsic_y = extrinsic_y_origin + ((j - _range // 2) / 10)

            extrinsic_matrix = np.array([[0, -1, 0, extrinsic_x * 0.001],
                                         [-1, 0, 0, extrinsic_y * 0.001],
                                         [0, 0, -1, extrinsic_z_origin],
                                         [0, 0, 0, 1]])

            # rotate by extrinsic center
            degree = 4

            img1 = rotate_tcp_pi(pidevice, vid, [0, 0, target_z, 0, 0, degree], extrinsic_matrix)
            img2 = rotate_tcp_pi(pidevice, vid, [0, 0, target_z, 0, 0, -degree], extrinsic_matrix)

            # sift -> to find three same points
            pts1, pts2 = sift(img1, img2)

            # get affine matrix
            M = cv2.getAffineTransform(pts1.astype(np.float32), pts2.astype(np.float32))
            norm = np.norm(M[:, 2]) - 0

            func_map[i, j] = norm
            print(norm)

    print('func', func_map)

    with open('func_map.npy', 'wb') as f:
        np.save(f, func_map)


def rotate_tcp_pi(pidevice, vid, pose, extrinsic_matrix):
    rotate_tcp = pose
    rotate_pi = ...
    mov(pidevice, rotate_pi)
    time.sleep(0.2)
    img2 = vid.read()
    return img2


if __name__ == '__main__':
    main()


