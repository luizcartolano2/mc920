from numpy import shape, empty

def encodeImage(imageMatrix, binaryText, bitPlane):
	"""

		Method to encode a string text in binary code into the image.

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
					encodedImage[h][w][c] = (imageMatrix[h][w][c] & ~(mask)) | (bit << bitPlane)

					count = count + 1
				else:
					# ja encodou o texto todo
					return encodedImage

	return encodedImage

def decodeImage(imageMatrix, bitPlane):
	"""

		Method to decode the text inside the image to a text string.

	    Parameters
	    ----------
		    imageMatrix : list
		        A list of ints with the matrix of pixels of the image to be modified

		    bitPlane : int
		        The bit plane where the text is encoded

	    Returns
	    -------
    		text : str
    			The decode text from the image
    """
	
	height, width, channel = imageMatrix.shape
	count = 0
	
	mask = 1 << bitPlane
	bits = ''
	text = ''
	chars = []

	for h in range(height):
		for w in range(width):
			for c in range(channel):
				pixel = imageMatrix[h][w][c]			
	
				bit = ( (pixel & mask) >> bitPlane) % 2
				bits = str(bits) + str(bit)
				count = count + 1

				if count == 8:
					# chars.append(chr(int(bits,2)))
					char = chr(int(bits,2))
					text = text + str(char)
					bits = ''
					count = 0

	
	# text = ''.join(chars)

	return text