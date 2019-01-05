__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "terminated"
__version__ = "1.0"
__date__    = ""

try:
    import re
except ImportError:
    raise SystemExit


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


def changeNewLine(originalFile, destFile):
    """

    :param originalFile: The file location of the input text
    :param destFile: The file location of the output text
    :return: Nothing

    """
    with open(originalFile, 'r') as myfile:
        data = myfile.read()

    data = re.sub(r"[^a-zA-Z0-9]", "", data)

    file = open(destFile, 'w')
    file.write(data)
    file.close()


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
