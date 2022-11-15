import time

from pi_init import pi_init, mov
from autofocus import AutoFocus, VideoCapture, waiting
from intrinsic import calc
import cv2


def main():
    magnification = 10
    # 0) init
    # pi
    pidevice = pi_init()

    # video capture
    vid = VideoCapture()
    waiting(vid)

    # 1) focus
    af = AutoFocus(magnification)
    target_z = af.autofocus_simple(pidevice, vid)
    time.sleep(1)

    # 2) workflow
    img1 = vid.read()
    dist = 0.5

    mov(pidevice, [0, dist, target_z, 0, 0, 0])
    time.sleep(1)

    img2 = vid.read()

    # mov(pidevice, [0, -dist, target_z, 0, 0, 0])
    # time.sleep(1)
    #
    # img3 = vid.read()

    # 3) calc
    calc(img1, img2, dist)


if __name__ == '__main__':
    main()
