# __Author__: Ao Xu

from __future__ import print_function
from pipython import GCSDevice, pitools
# import matlab
# import matlab.engine
import numpy as np
# from realsense import get_color_depth, stop_pipeline
import cv2


# __signature__ = 0xdcb05d1beb5fa4c6d4636397b624d18f

CONTROLLERNAME = 'C-887'
STAGES = None  # set something like ('M-122.2DD', 'M-122.2DD') if your stages need CST
REFMODES = ['FRF', ]  # reference first axis or hexapod

# get camera intrinsic
# k = [614.2276611328125, 0.0, 327.88189697265625, 0.0, 613.449462890625, 239.263671875, 0.0, 0.0, 1.0]
# k = [[-614.227, 0.0, 0.0], [0.0, -613.449, 0.0], [327.881, 239.263, 1.0]]

# open target image
# target = cv2.imread('img_Color.png')
# target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)


# def main(pidevice):
#     # start pi
#     pidevice.ConnectTCPIP(ipaddress='192.168.10.100', ipport=50000)
#     pitools.startup(pidevice, stages=STAGES, refmodes=REFMODES)
#     print('pi initialed')
#
#     # set init pose
#     # pose_init = [1, 2, 3, 4, 2, 4]
#     pose_init = [0, 0, 0, 5, 5, 5]
#     mov(pidevice, pose_init)
#     print('set to init pose')
#
#     # start matlab
#     engine = matlab.engine.start_matlab('MATLAB_R2022b')
#     print('matlab initialed')
#
#     while True:
#         # get pose
#         pose0 = get_pose(pidevice)
#         pose0 = [pose0['X'], pose0['Y'], pose0['Z'], pose0['U'], pose0['V'], pose0['W']]
#         # print(pose0)
#
#         # get realsense image
#         color, depth = get_color_depth()
#         color_gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
#
#         pose = np.array(engine.servo_step(matlab.double(pose0),
#                                           matlab.double(k),
#                                           matlab.double(color_gray.tolist()),
#                                           matlab.double(depth.tolist()),
#                                           matlab.double(target_gray.tolist())
#                                           ))
#         # pose = [pose[0][0], pose[1][0], pose[2][0], pose[3][0], pose[4][0], pose[5][0]]
#         pose = [0, 0, 0, pose[3][0], pose[4][0], pose[5][0]]
#         print('pose:', pose)
#
#         # publish pose
#         mov(pidevice, pose)
#
#         # display
#         cv2.namedWindow('PI SERVO', cv2.WINDOW_NORMAL)
#         cv2.imshow('PI SERVO', color)
#         key = cv2.waitKey(1)
#
#         if key & 0xFF == ord('q') or key == 27:
#             cv2.destroyAllWindows()
#             break
#
#     stop_pipeline()
#
#     pose_init = [0, 0, 0, 0, 0, 0]
#     mov(pidevice, pose_init)


def get_pose(pidevice):
    pos = pidevice.qPOS()
    return pos


def mov(pidevice, pose):
    pidevice.MOV(pidevice.axes[0:6], pose)
    pitools.waitontarget(pidevice, pidevice.axes[0:6])


def pi_init():
    pidevice = GCSDevice(CONTROLLERNAME)
    pidevice.ConnectTCPIP(ipaddress='192.168.10.100', ipport=50000)
    pitools.startup(pidevice, stages=STAGES, refmodes=REFMODES)
    # pose_init = [0, 0, 0, 0, 0, 0]
    # mov(pidevice, pose_init)
    print('pi initialed')
    return pidevice


# if __name__ == '__main__':
#     with GCSDevice(CONTROLLERNAME) as pidevice:
#         main(pidevice)
