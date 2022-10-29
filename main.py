# import the opencv library
from pi_init import pi_init, get_pose, mov
from autofocus import AutoFocus, VideoCapture
import matlab
import matlab.engine
import cv2
import numpy as np


def main():
    vid = VideoCapture()
    pidevice = pi_init()

    # object lens: len length, working distance
    # 4: 28.5, 17.35
    # 10: 30.5, 17
    # 20: 42.5, 3.6
    # 40: 45, 0.56
    # 60: 45, 0.19

    # AutoFocus.autofocus_simple(pidevice)
    AutoFocus.autofocus_simple(pidevice, vid, 42.5, 3.6)
    servo(pidevice, vid, k, target)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def servo(pidevice, vid, k, target):
    # start matlab
    engine = matlab.engine.start_matlab('MATLAB_R2022b')
    print('matlab initialed')

    while True:
        # get pose
        pose0 = get_pose(pidevice)
        pose0 = [pose0['X'], pose0['Y'], pose0['Z'], pose0['U'], pose0['V'], pose0['W']]
        # print(pose0)

        # get realsense image
        color = vid.read()
        color_gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

        pose = np.array(engine.servo_step(matlab.double(pose0),
                                          matlab.double(k),
                                          matlab.double(color_gray.tolist()),
                                          # matlab.double(depth.tolist()),
                                          matlab.double(target_gray.tolist())
                                          ))
        # pose = [pose[0][0], pose[1][0], pose[2][0], pose[3][0], pose[4][0], pose[5][0]]
        pose = [0, 0, 0, pose[3][0], pose[4][0], pose[5][0]]
        print('pose:', pose)

        # publish pose
        mov(pidevice, pose)

        # display
        cv2.imshow('MICRO SERVO', color)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()



