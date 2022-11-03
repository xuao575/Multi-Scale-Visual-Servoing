from pi_init import mov
import cv2
import numpy as np
import queue
import threading

class AutoFocus:
    @staticmethod
    def autofocus_simple(pidevice, vid, length=30.5, working_dist=17, half_range=0.2, step=0.02):
        # vid = cv2.VideoCapture(0)
        # vid = VideoCapture()

        total = 51.5
        slide = 1
        space = total - length
        d = space - (slide + working_dist)
        zs = np.arange(-(d - half_range), -(d + half_range), -step)
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

            cv2.imshow('rgb', img)
            cv2.waitKey(1)
            # cv2.destroyWindow()

        target_ind = np.argmax(contrasts)
        target_z = zs[target_ind]

        mov(pidevice, [0, 0, target_z, 0, 0, 0])
        img = vid.read()
        cv2.imshow(f'{np.round(target_z,2)}_finish', img)
        cv2.waitKey(10)

        # cv2.destroyAllWindows()

        return target_z


class VideoCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
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
