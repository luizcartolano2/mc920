from numpy import shape, empty

def encodeImage(imageMatrix, binaryText, bitPlane):
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