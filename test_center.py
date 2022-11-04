import cv2
import numpy as np


figure_1 = cv2.imread('figure 2.png')
figure_2 = cv2.imread('figure 17.png')


# Define the 3 pairs of corresponding points
input_pts = np.float32([[378,337], [394, 268], [290, 93]])
output_pts = np.float32([[340,307], [352, 236], [239, 73]])

# print(input_pts)

# Calculate the transformation matrix using cv2.getAffineTransform()
M = cv2.getAffineTransform(input_pts, output_pts)

print(np.dot(M, np.transpose([225,378,1])))

print(M)
