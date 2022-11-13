import cv2
from autofocus import VideoCapture, waiting
import time

vid = VideoCapture()
waiting(vid)

img = vid.read()
cv2.imwrite(f'{time.time()}.png', img)

cv2.imshow('sampling', img)
cv2.waitKey(0)

