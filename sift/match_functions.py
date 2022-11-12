import numpy as np
import cv2


def common_dispose(image, feature_width):
    image = cv2.copyMakeBorder(np.uint8(image * 255.0), int(feature_width / 2), int(feature_width / 2),
                               int(feature_width / 2), int(feature_width / 2), borderType=cv2.BORDER_REFLECT)

    # Step 1: Conduct Gaussian Blur.
    image_blur = cv2.GaussianBlur(image, ksize=(3, 3), sigmaX=1, sigmaY=1)

    # Step 2: Calculate the image gradient.
    dx, dy = cv2.spatialGradient(image_blur, ksize=3)
    dx = dx.astype(np.int32)
    dy = dy.astype(np.int32)
    return dx, dy


def get_interest_points(image, feature_width):
    """ Returns a set of interest points for the input image
    Args:
        image - can be grayscale or color, your choice.
        feature_width - in pixels, is the local feature width. It might be
            useful in this function in order to (a) suppress boundary interest
            points (where a feature wouldn't fit entirely in the image)
            or (b) scale the image filters being used. Or you can ignore it.
    Returns:
        x and y: nx1 vectors of x and y coordinates of interest points.
        confidence: an nx1 vector indicating the strength of the interest
            point. You might use this later or not.
        scale and orientation: are nx1 vectors indicating the scale and
            orientation of each interest point. These are OPTIONAL. By default you
            do not need to make scale and orientation invariant local features. 
    """
    h, w = image.shape[:2]
    dx, dy = common_dispose(image, feature_width)

    # Placeholder that you can delete -- these are just random points
    # x = np.ceil(np.random.rand(500, 1) * w)
    # y = np.ceil(np.random.rand(500, 1) * h)


    # Step 3: Build a 2D Gaussian function as the window function.
    Gkernel_1D = cv2.getGaussianKernel(ksize=feature_width + 1, sigma=feature_width / 2, ktype=cv2.CV_32F)
    Gkernel_2D = Gkernel_1D * np.transpose(Gkernel_1D)

    # Step 4: Calculate the structure tensor and the corner response.
    response = np.zeros((h, w), dtype=np.float64)
    # Empirical constant for response function.
    k = 0.06
    # Threshold for response function.
    threshold = 1000000
    for i in range(h):
        for j in range(w):
            M = np.zeros((2, 2), dtype=np.float32)
            M[0, 0] = np.sum(dx[int(i) : int(i + feature_width + 1), int(j) :int(j + feature_width + 1)] ** 2 * Gkernel_2D)
            M[0, 1] = np.sum(dx[int(i) : int(i + feature_width + 1), int(j) : int(j + feature_width + 1)] * dy[int(i) : int(i + feature_width + 1), int(j) : int(j + feature_width + 1)] * Gkernel_2D)
            M[1, 0] = M[0, 1]
            M[1, 1] = np.sum(dy[int(i) : int(i + feature_width + 1), int(j) : int(j + feature_width + 1)] ** 2 * Gkernel_2D)

            if (np.linalg.det(M) - k * (np.trace(M)) ** 2) > threshold:
                response[i][j] = np.linalg.det(M) - k * (np.trace(M)) ** 2

    # Step 5: Detect features that are local maxima within a radius r.
    # Radius of Detection region.
    r = 1
    x = []
    y = []
    response = np.pad(response, ((int(r), int(r)), (int(r), int(r))), 'edge')
    for i in range(h):
        for j in range(w):
            local_region = response[i : int(i + 2 * r + 1), j : int(j + 2 * r + 1)]
            if local_region.max() == response[int(i + r)][int(j + r)] and response[int(i + r)][int(j + r)] > 0:
                y.append([i])
                x.append([j])

    # If you do not use (confidence, scale, orientation), just delete
    # return x, y, confidence, scale, orientation
    x = np.array(x)
    y = np.array(y)

    return x, y


def get_features(image, x, y, feature_width):
    """ Returns a set of feature descriptors for a given set of interest points. 
    Args:
        image - can be grayscale or color, your choice.
        x and y: nx1 vectors of x and y coordinates of interest points.
            The local features should be centered at x and y.
        feature_width - in pixels, is the local feature width. You can assume
            that feature_width will be a multiple of 4 (i.e. every cell of your
            local SIFT-like feature will have an integer width and height).
        If you want to detect and describe features at multiple scales or
            particular orientations you can add other input arguments.
    Returns:
        features: the array of computed features. It should have the
            following size: [length(x) x feature dimensionality] (e.g. 128 for
            standard SIFT)
    """
    # Placeholder that you can delete. Empty features.
    features = np.zeros((x.shape[0], 128))
    dx, dy = common_dispose(image, feature_width)

    # Step 3: Calculate the magnitude and orientation of each pixel.
    mag = np.sqrt(dx ** 2 + dy ** 2)
    orient = np.arctan2(dy, dx) + np.pi

    # Step 4: Build a 2D Gaussian function with kernel size equal to n and standard deviation to be n / 2.
    Gkernel_1D = cv2.getGaussianKernel(ksize=feature_width + 1, sigma=feature_width / 2, ktype=cv2.CV_32F)
    Gkernel_2D = Gkernel_1D * np.transpose(Gkernel_1D)

    # Step 5: Extract un-normalized features.
    for i in range(x.shape[0]):
        window_mag = mag[int(y[i]) : int(y[i] + feature_width + 1), int(x[i]) : int(x[i] + feature_width + 1)] * Gkernel_2D
        window_orient = orient[int(y[i]) : int(y[i] + feature_width + 1), int(x[i]) : int(x[i] + feature_width + 1)]
        for cell_x in range(4):
            for cell_y in range(4):
                bin = np.zeros(8)
                cell_mag = window_mag[int(cell_y * feature_width / 4 + cell_y // 2) : int((cell_y + 1) * feature_width / 4 + cell_y // 2), int(cell_x * feature_width / 4 + cell_x // 2) : int((cell_x + 1) * feature_width / 4 + cell_x // 2)].flatten()
                cell_orient = window_orient[int(cell_y * feature_width / 4 + cell_y // 2) : int((cell_y + 1) * feature_width / 4 + cell_y // 2), int(cell_x * feature_width / 4 + cell_x // 2) : int((cell_x + 1) * feature_width / 4 + cell_x // 2)].flatten()
                for j in range(len(cell_orient)):
                    if int(cell_orient[j] // (np.pi / 4)) > 7:
                        bin[7] += cell_mag[j]
                    else:
                        bin[int(cell_orient[j] // (np.pi / 4))] += cell_mag[j]
                features[i, cell_x * 32 + cell_y * 8 : cell_x * 32 + cell_y * 8 + 8] = bin

    # Step 6: Normalize the features vector.
        features[i] = features[i] / np.linalg.norm(features[i])

    return features


def match_features(features1, features2, threshold=0.0):
    """ 
    Args:
        features1 and features2: the n x feature dimensionality features
            from the two images.
        threshold: a threshold value to decide what is a good match. This value 
            needs to be tuned.
        If you want to include geometric verification in this stage, you can add
            the x and y locations of the features as additional inputs.
    Returns:
        matches: a k x 2 matrix, where k is the number of matches. The first
            column is an index in features1, the second column is an index
            in features2. 
        Confidences: a k x 1 matrix with a real valued confidence for every
            match.
        matches' and 'confidences' can be empty, e.g. 0x2 and 0x1.
    """

    # Placeholder that you can delete. Random matches and confidences
    # num_features = min(features1.shape[0], features2.shape[0])
    # matched = np.zeros((num_features, 2))
    # matched[:, 0] = np.random.permutation(num_features)
    # matched[:, 1] = np.random.permutation(num_features)
    # confidence = np.random.rand(num_features, 1)
    num_features = max(features1.shape[0], features2.shape[0])
    matched = np.zeros((num_features, 2))
    confidence = np.zeros((num_features, 1))

    for m in range(features1.shape[0]):
        dists = np.sqrt(np.sum(np.power(features1[m] - features2, 2), axis=1))
        dists_order = np.argsort(dists)
        nearest_dist = dists[dists_order[0]] if dists[dists_order[0]] > 0 else 0.01
        sec_nearest_dist = dists[dists_order[1]]
        confidence[m] = sec_nearest_dist / nearest_dist
        matched[m, 0] = m
        matched[m, 1] = dists_order[0]

    # Sort the matches so that the most confident onces are at the top of the
    # list. You should probably not delete this, so that the evaluation
    # functions can be run on the top matches easily.
    order = np.argsort(confidence, axis=0)[::-1, 0]
    confidence = confidence[order, :]
    matched = matched[order, :]

    for indice in range(num_features):
        if confidence[indice] < threshold:
            break
        real_num_features = indice + 1
    confidence = confidence[:real_num_features]
    matched = matched[:real_num_features, :]

    return matched, confidence