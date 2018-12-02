import cv2
import numpy as np
from matplotlib.pyplot import imshow, show

######################################################################
# 	Method to read an image 										 #
#																	 #	
#    Parameters 													 #
#   ----------														 #
#	    filename : str 												 #
#	        The file location of the image 							 #
#																	 #
#   Returns 														 #
#    -------														 #
#	    list 														 #
#	        A list of ints with the matrix of pixels of the image.   #
######################################################################
def readImage(filename):
	# read the image
	image_matrix = cv2.imread(filename,1)
	img = image_matrix.astype(dtype='uint8')
	# return the image readed
	return img

def storeImage(filename, image_matrix):
	"""

		Method to store new images

	    Parameters
	    ----------
		    filename : str
		        The file location of the image
		    image_matrix : list
		    	A list of ints with the matrix of pixels of the image

	    Returns
	    -------
		    Nothing
    
    """

	cv2.imwrite(filename, image_matrix)