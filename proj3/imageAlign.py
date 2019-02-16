__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "terminated"
__version__ = "1.0"
__date__    = "12 december 2018"

try:
    import cv2
    import numpy as np
    import statistics
    import skimage as sk
except ImportError:
    raise SystemExit


def hough_transform(img_matrix):
    """

    Function that calculate the angle rotation according to the Hough Transform technique

    :param img_matrix: A list of ints with the matrix of pixels of the image
    :return: medianAngle: angle of rotation

    """
    try:
        gray_matrix = cv2.cvtColor(img_matrix, cv2.COLOR_BGR2GRAY)
        image_edges = cv2.Canny(gray_matrix, 50, 150, apertureSize=3)

        image_lines = cv2.HoughLinesP(image_edges, 1, np.pi/180.0, 100, minLineLength=100, maxLineGap=5)
    except:
        return None

    image_angles = []
    for line in image_lines:
        for x1,y1,x2,y2 in line:
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            image_angles.append(angle)

    median_angle = statistics.median(image_angles)

    return median_angle


def horizontal_projection(img_matrix):
    """

    Function that calculate the angle rotation according to the Hough Transform technique

    :param img_matrix: A list of ints with the matrix of pixels of the image
    :return: rotateAngle: angle of rotation

    """
    try:
        img_grey = cv2.cvtColor(img_matrix, cv2.COLOR_BGR2GRAY)
        img_matrix = cv2.adaptiveThreshold(src=img_grey, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           thresholdType=cv2.THRESH_BINARY_INV, blockSize=17, C=10)
    except:
        return None

    temp_valor = 0
    theta_max = 0

    for theta in range(-90, 90):
        try:
            rot = sk.transform.rotate(image=img_matrix, angle=theta, resize=True, clip=False, preserve_range=True)
        except:
            return None

        perfil = np.sum(rot, axis=1)
        valor = np.max(perfil)

        if valor > temp_valor:
            temp_valor = valor
            theta_max = theta

    return theta_max
