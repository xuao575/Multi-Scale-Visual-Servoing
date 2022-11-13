import cv2
import time
from serialport import COM
from main import rotate_lens
from autofocus import AutoFocus, VideoCapture, waiting
from pi_init import pi_init


def sample():
    lens = [10, 20, 40]
    pidevice = pi_init()

    vid = VideoCapture()
    waiting(vid)

    motor_com = COM('COM4', 9600)
    milli_time = time.time()

    for i, magnification in enumerate(lens):
        af = AutoFocus(magnification)
        af.autofocus_simple(pidevice, vid)

        img = vid.read()
        cv2.imwrite(f'{milli_time}_{i}.png', img)

        cv2.imshow(f'{milli_time}_{i}.png', img)
        cv2.waitKey(100)

        rotate_lens(motor_com, i)


if __name__ == '__main__':
    sample()
