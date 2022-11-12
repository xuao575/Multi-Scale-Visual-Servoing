from pi_init import pi_init, get_pose, mov
from autofocus import AutoFocus, VideoCapture, waiting
import matlab
import matlab.engine
import cv2
import numpy as np
from extrinsic import extrinsic_optimize


def main():
    # init
    pidevice = pi_init()

    engine = matlab.engine.start_matlab('MATLAB_R2022b')
    engine.cd('servo', nargout=0)

    vid = VideoCapture()
    waiting(vid)

    # 1) optimize extrinsic
    extrinsic_optimize()

    for magnification in [10]:
        # choose lens
        af = AutoFocus(magnification)

        # 2) focus
        target_z = af.autofocus_simple(pidevice, vid)

        # 3) pi servo
        target = cv2.imread('figure 6.png')
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

        cv2.imshow('target', target)
        cv2.waitKey(100)

        servo(pidevice, engine, vid, af, target_gray, target_z)


def servo(pidevice, engine, vid, af, target_gray, target_z):
    color = vid.read()
    depth_map = np.ones(color.shape[0:2]) * af.working_dist * 0.001

    while True:
        # get pose
        pose0 = get_pose(pidevice)
        pose0 = [pose0['X'], pose0['Y'], pose0['Z'], pose0['U'], pose0['V'], pose0['W']]

        color = vid.read()
        color_gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

        # display
        cv2.imshow('MICRO SERVO', color)
        cv2.waitKey(1)

        pose = np.array(engine.servoS(matlab.double(pose0),
                                      matlab.double(af.k),
                                      matlab.double(color_gray.tolist()),
                                      matlab.double(depth_map.tolist()),
                                      matlab.double(target_gray.tolist())
                                      ))

        pose = [np.clip(pose[0][0], -12, 12), np.clip(pose[1][0], -12, 12), target_z, 0, 0, np.clip(pose[5][0], -5, 5)]
        print('pose:', pose)

        mov(pidevice, pose)


if __name__ == '__main__':
    main()



