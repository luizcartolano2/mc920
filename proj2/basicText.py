import re

def txtToBin(filename):
	"""

		Method to convert a string text in binary code.

	    Parameters
	    ----------
		    filename : str
		        The file location of the text

	    Returns
	    -------
		    binarray : str
		    	The string representation of the text in binary code
    
    """

	with open(filename, 'r') as txtFile:
		text = txtFile.read()

	binarray = ''.join(format(ord(char), '08b') for char in text)

	return binarray

#########################################################################
#
#	Method to eliminate spaces and special characters in a file text.
#
#   Parameters
#    ----------
#	    originalFile : str
#	        The file location of the input text
#	    destFile : str
#	        The file location of the output text
#
#    Returns
#    -------
#	    Nothing
#########################################################################
def changeNewLine(originalFile, destFile):

    with open(originalFile, 'r') as myfile:
        data=myfile.read()

    data = re.sub(r"[^a-zA-Z0-9]","",data)

    file = open(destFile, 'w')
    file.write(data)
    file.close

def writeText(filename, data):
	"""

		Method to write text into a file.

	    Parameters
	    ----------
		    filename : str
		        The file location of the input text
		    data : str
		        The text to be write into the file

	    Returns
	    -------
		    Nothing
    
    """

	with open(filename, 'w+') as writeFile:
		writeFile.write(data)
