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

def rotateImage(imgMatrix, rotAngle):

	#	pega a altura e largura da imagem
	height, width = imgMatrix.shape[:2]
	# 	pega o ponto central da imagem
	centralPoint = (width / 2, height / 2)

	rotation = cv2.getRotationMatrix2D(centralPoint, rotAngle, 1.0)
	rotated = cv2.warpAffine(imgMatrix, rotation, (width, height))

	cv2.imshow("Rotacionado ", rotated)
 
	cv2.waitKey(0)

	return rotated