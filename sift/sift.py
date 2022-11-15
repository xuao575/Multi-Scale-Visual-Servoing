import cv2
import numpy as np
import sift.match_functions as mf
from sift.utils import *


def sift(img1, img2, num_pts_to_evaluate=3):
    """

    :param img1:
    :param img2:
    :param num_pts_to_evaluate:
    :return: pts: (100, 2) ndarray in image 1, (100, 2) ndarray in image 2
    """
    image1 = img1
    image2 = img2

    # make images smaller to speed up the algorithm
    scale_factor = 1
    if scale_factor != 1:
        image1 = cv2.resize(image1, (0, 0), fx=scale_factor, fy=scale_factor,
                            interpolation=cv2.INTER_LINEAR)
        image2 = cv2.resize(image2, (0, 0), fx=scale_factor, fy=scale_factor,
                            interpolation=cv2.INTER_LINEAR)

    # change to gray-scale images
    image1_bw = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_bw = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # width and height of each local feature, in pixels.
    feature_width = 16

    # 2) Find distinctive points in each image.
    print('SIFT - getting interest points...')
    x1, y1 = mf.get_interest_points(image1_bw, feature_width=6)
    x2, y2 = mf.get_interest_points(image2_bw, feature_width=6)

    # 3) Create feature vectors at each interest point.
    print('SIFT - getting features...')
    image1_features = mf.get_features(image1_bw, x1, y1, feature_width)
    image2_features = mf.get_features(image2_bw, x2, y2, feature_width)

    # 4) Match features.
    print('SIFT - matching features...')
    matches, _ = mf.match_features(image1_features, image2_features)

    # m -> match
    x1_m = x1[matches[:num_pts_to_evaluate, 0].astype(np.int32)]
    y1_m = y1[matches[:num_pts_to_evaluate, 0].astype(np.int32)]

    x2_m = x2[matches[:num_pts_to_evaluate, 1].astype(np.int32)]
    y2_m = y2[matches[:num_pts_to_evaluate, 1].astype(np.int32)]

    # pick three sparse points
    # x1_t, y1_t = pick_points(x1_m, y1_m, num_pts_to_evaluate)
    # x2_t, y2_t = pick_points(x2_m, y2_m, num_pts_to_evaluate)

    # draw correspondence
    # show_correspondence2(image1, image2, x1_m, y1_m, x2_m, y2_m, 'result')

    return np.concatenate((x1_m, y1_m), axis=1), np.concatenate((x2_m, y2_m), axis=1)


if __name__ == '__main__':
    # 1) Loads and resizes images
    img1 = cv2.imread('figure 1.png').astype('single')
    img2 = cv2.imread('figure 7.png').astype('single')
    pts1, pts2 = sift(img1, img2)
    print(pts1, pts2)



