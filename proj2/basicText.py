import re

def txtToBin(filename):
	with open(filename, 'r') as txtFile:
		text = txtFile.read()

	binarray = ''.join(format(ord(char), '08b') for char in text)

	return binarray

def changeNewLine(originalFile, destFile):

    with open(originalFile, 'r') as myfile:
        data=myfile.read()

    data = re.sub(r"[^a-zA-Z0-9]","",data)

    file = open(destFile, 'w')
    file.write(data)
    file.close
