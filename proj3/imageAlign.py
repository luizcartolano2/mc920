import cv2
import numpy as np
import statistics

def houghTransform(imgMatrix):

	grayMatrix = cv2.cvtColor(imgMatrix, cv2.COLOR_BGR2GRAY)
	imageEdges = cv2.Canny(grayMatrix,50,150,apertureSize = 3)

	imageLines = cv2.HoughLinesP(imageEdges, 1, np.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

	imageAngles = []
	for line in imageLines:
		for x1,y1,x2,y2 in line:
			angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
			imageAngles.append(angle)

	medianAngle = statistics.median(imageAngles)

	return medianAngle