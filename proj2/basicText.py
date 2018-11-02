def txtToBin(filename):
	with open(filename, 'r') as txtFile:
		text = txtFile.read()

	binarray = ' '.join(format(ch, 'b') for ch in bytearray(text))
	
	return binarray

def changeNewLine(originalFile, destFile):

    with open(originalFile, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    file = open(destFile, 'w')
    file.write(data)
    file.close
