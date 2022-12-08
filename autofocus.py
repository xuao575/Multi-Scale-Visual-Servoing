import imutils
from pi_init import mov
import cv2
import numpy as np
import queue
import threading
import time

class AutoFocus:
    # object lens: recommended working z
    params = {10: {'rec_z': -3., 'rec_y': 0.4, 'scan_range': 0.4, 'step': 0.01,
                   'k': [[-7634.29, 0.0, 320.0], [0.0, -7634.29, 240.0], [0.0, 0.0, 1.0]]},
              20: {'rec_z': -4.54, 'rec_y': 0.2, 'scan_range': 0.3, 'step': 0.01,
                   'k': [[-7634.29, 0.0, 320.0], [0.0, -7634.29, 240.0], [0.0, 0.0, 1.0]]},
              40: {'rec_z': -4.815, 'rec_y': 0.1, 'scan_range': 0.2, 'step': 0.005,
                   'k': [[-7634.29, 0.0, 320.0], [0.0, -7634.29, 240.0], [0.0, 0.0, 1.0]]},
              }

    def __init__(self, magnification):
        self.magnification = magnification
        self.rec_z = AutoFocus.params[magnification]['rec_z']
        self.rec_y = AutoFocus.params[magnification]['rec_y']
        self.scan_range = AutoFocus.params[magnification]['scan_range']
        self.step = AutoFocus.params[magnification]['step']
        self.k = AutoFocus.params[magnification]['k']

    def autofocus_simple(self, pidevice, vid):

        zs = np.arange(self.rec_z + self.scan_range / 2., self.rec_z - self.scan_range / 2., -self.step)
        contrasts = []

        for z in zs:
            mov(pidevice, [0, 0, z, 0, 0, 0])
            img = vid.read()
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # mean = img_gray.std()

            laplacian = cv2.Laplacian(img_gray, cv2.CV_16U)
            dst = cv2.convertScaleAbs(laplacian)
            mean = np.mean(dst)

            contrasts.append(mean)

            cv2.imshow('focus', img)
            cv2.waitKey(1)

        cv2.destroyWindow('focus')

        target_ind = np.argmax(contrasts)
        target_z = zs[target_ind]

        mov(pidevice, [0, 0, target_z, 0, 0, 0])
        # img = vid.read()
        # cv2.imshow(f'{np.round(target_z,2)}_finish', img)
        # cv2.waitKey(100)

        return target_z


class VideoCapture:
    def __init__(self, ind):
        self.cap = cv2.VideoCapture(ind)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FPS, 10)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()

def regulate_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rsz = imutils.resize(gray, width=640)
    crop = rsz[:, 140:500]
    return crop

def shot():
    vid = VideoCapture(0)
    img = vid.read()
    img = regulate_image(img)
    cv2.imwrite(f'{int(time.time())}.png', img)

    # vid = VideoCapture(0)
    # while True:
    #     img = vid.read()
    #     img = regulate_image(img)
    #     cv2.imshow('input', img)
    #     cv2.waitKey(1)

def waiting(vid):
    mean = -1
    while mean < 100:
        img = vid.read()
        cv2.imshow('waiting', img)
        cv2.waitKey(1)
        mean = np.mean(img)
    print('program started')
    cv2.destroyWindow('waiting')

if __name__ == '__main__':
    shot()