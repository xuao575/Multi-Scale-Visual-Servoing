import numpy as np
from pi_init import get_pose, mov
import cv2
import matlab


def servo(pidevice, engine, vid, af, target_gray, target_z):
    color = vid.read()
    depth_map = np.ones(color.shape[0:2]) * 1 * 0.001

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
        pose[5] = 0
        print('pose:', pose)

        mov(pidevice, pose)
