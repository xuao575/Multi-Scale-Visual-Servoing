import numpy as np
import cv2 as cv

filename = 'target.png'
img = cv.imread(filename)
# gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = np.float32(img)
dst = cv.cornerHarris(gray,3,3,cv.BORDER_REFLECT)
#result is dilated for marking the corners, not important
dst = cv.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]
cv.imshow('dst',img)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()