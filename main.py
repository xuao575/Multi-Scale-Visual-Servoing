import time

from pi_init import pi_init
from autofocus import AutoFocus, VideoCapture, waiting
import matlab
import matlab.engine
import cv2
from extrinsic import extrinsic_optimize
from serialport import COM
from servo.pi_servo import servo


def main():
    lens = [10, 20, 40]
    # 0) init
    # pi
    pidevice = pi_init()

    # matlab
    engine = matlab.engine.start_matlab('MATLAB_R2022b')
    engine.cd('servo', nargout=0)

    # video capture
    vid = VideoCapture()
    waiting(vid)

    # motor serial
    motor_com = COM('COM4', 9600)

    # 1) optimize extrinsic
    extrinsic_optimize()

    for i, magnification in enumerate(lens):
        # choose lens
        af = AutoFocus(magnification)

        # 2) focus
        target_z = af.autofocus_simple(pidevice, vid)

        # 3) pi servo
        target = cv2.imread(f'target{i}.png')
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

        cv2.imshow(f'target{i}', target)
        cv2.waitKey(100)

        servo(pidevice, engine, vid, af, target_gray, target_z)

        # 4) rotate lens
        rotate_lens(motor_com, i)


def rotate_lens(motor_com, i):
    assert i < 3
    motor_com.open()
    if i < 2:
        motor_com.send_data('01220\n')  # anti clock-wise 120.0 degree
    else:
        motor_com.send_data('12460\n')  # clock-wise to origin
    time.sleep(15)
    motor_com.close()


if __name__ == '__main__':
    main()



