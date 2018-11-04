import cv2
import numpy as np
from matplotlib.pyplot import imshow, show

def readImage(filename):
	 """
	 	Method to read an image

	    Parameters
	    ----------
		    filename : str
		        The file location of the image

	    Returns
	    -------
		    list
		        A list of ints with the matrix of pixels of the image

    """

	# path to the file
	filename = filename
	# read the image
	image_matrix = cv2.imread(filename)
	# return the image readed
	return image_matrix

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

def writePlans(img):
	"""

		Method to show specific planes of the image

	    Parameters
	    ----------
		    img : list
		    	A list of ints with the matrix of pixels of the image

	    Returns
	    -------
		    Nothing
    
    """

	first_plane = np.empty(img.shape)
	second_plane = np.empty(img.shape)
	third_plane = np.empty(img.shape)
	last_plane = np.empty(img.shape)

	first_plane[:, :, 2] = ((img[:,:,2] >> 0) % 2) * 255
	first_plane[:, :, 1] = ((img[:,:,1] >> 0) % 2) * 255
	first_plane[:, :, 0] = ((img[:,:,0] >> 0) % 2) * 255
	imshow(first_plane)
	show()

	second_plane[:, :, 2] = ((img[:,:,2] >> 1) % 2) * 255
	second_plane[:, :, 1] = ((img[:,:,1] >> 1) % 2) * 255
	second_plane[:, :, 0] = ((img[:,:,0] >> 1) % 2) * 255
	imshow(second_plane)
	show()

	third_plane[:, :, 2] = ((img[:,:,2] >> 2) % 2) * 255
	third_plane[:, :, 1] = ((img[:,:,1] >> 2) % 2) * 255
	third_plane[:, :, 0] = ((img[:,:,0] >> 2) % 2) * 255
	imshow(third_plane)
	show()

	last_plane[:, :, 2] = ((img[:,:,2] >> 7) % 2) * 255
	last_plane[:, :, 1] = ((img[:,:,1] >> 7) % 2) * 255
	last_plane[:, :, 0] = ((img[:,:,0] >> 7) % 2) * 255
	imshow(last_plane)
	show()
