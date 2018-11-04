from numpy import shape, empty, ndarray

def encodeImage(imageMatrix, binaryText, bitPlane):
	"""

		Method to convert a string text in binary code.

	    Parameters
	    ----------
		    imageMatrix : list
		        A list of ints with the matrix of pixels of the image to be modified

		    binaryText : str
		        The binary representation of the text to be encoded

		    bitPlane : int
		        The bit plane where the text will be encoded

	    Returns
	    -------
		    encodedImage : list
		    	A list of ints with the matrix of pixels of the image with text encoded
    
    """

	height, width, channel = imageMatrix.shape

	count = 0
	encodedImage = imageMatrix
	mask = 1 << bitPlane

	for h in range(height):
		for w in range(width):
			for c in range(channel):
				if count < len(binaryText):
					bit = int(binaryText[count])				
					encodedImage[h][w][c] = (encodedImage[h][w][c] & (~mask)) | bit
					count = count + 1
				else:
					# ja encodou o texto todo
					return encodedImage

	return encodedImage

def decodeImage():
	return