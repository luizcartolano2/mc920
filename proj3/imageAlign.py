import cv2
import numpy as np
import statistics
import skimage as sk

def houghTransform(imgMatrix):
    """

    Function that calculate the angle rotation according to the Hough Transform technique

    :param imgMatrix: A list of ints with the matrix of pixels of the image
    :return: medianAngle: angle of rotation

    """
    grayMatrix = cv2.cvtColor(imgMatrix, cv2.COLOR_BGR2GRAY)
    imageEdges = cv2.Canny(grayMatrix, 50, 150, apertureSize=3)

    imageLines = cv2.HoughLinesP(imageEdges, 1, np.pi/180.0, 100, minLineLength=100, maxLineGap=5)

    imageAngles = []
    for line in imageLines:
        for x1,y1,x2,y2 in line:
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            imageAngles.append(angle)

    medianAngle = statistics.median(imageAngles)

    return medianAngle


def horizontalProjection(imgMatrix):
    """

    Function that calculate the angle rotation according to the Hough Transform technique

    :param imgMatrix: A list of ints with the matrix of pixels of the image
    :return: rotateAngle: angle of rotation

    """
    imgGrey = cv2.cvtColor(imgMatrix, cv2.COLOR_BGR2GRAY)
    imgMatrix = cv2.adaptiveThreshold(src=imgGrey, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      thresholdType=cv2.THRESH_BINARY_INV, blockSize=17, C=10)

    tempValor = 0
    thetaMax = 0

    for theta in range(-90, 90):
        rot = sk.transform.rotate(image=imgMatrix, angle=theta, resize=True, clip=False, preserve_range=True)
        perfil = np.sum(rot, axis=1)
        valor = np.max(perfil)

        if valor > tempValor:
            tempValor = valor
            thetaMax = theta

    return thetaMax