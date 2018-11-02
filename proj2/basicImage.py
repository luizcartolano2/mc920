import cv2

""" Method to read an image """
def readImage(filename):
	# path to the file
	filename = filename
	# read the image
	image_matrix = cv2.imread(filename)
	# return the image readed
	return image_matrix

""" Method to store new modified images """
def storeImage(path, filename, image_matrix):
	filename = path + filename
	cv2.imwrite(filename, image_matrix)
