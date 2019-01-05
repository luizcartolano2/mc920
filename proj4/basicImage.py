__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "production"
__version__ = "1.1"
__date__    = ""

try:
    import cv2
    import numpy as np
except ImportError:
    raise SystemExit


def readImage(filename):
    """
    Method to read new images

    :param filename: The file location of the image
    :return: img: A list of ints with the matrix of pixels of the image

    """
    #   read the image
    try:
        image_matrix = cv2.imread(filename, 1)
        img = image_matrix.astype(dtype='uint8')
    except Exception:
        return np.array([])

    #   return the image readed
    return img


def storeImage(filename, image_matrix):
    """
    Method to store new images

    :param filename: The file location of the image
    :param image_matrix: A list of ints with the matrix of pixels of the image
    :return: None

    """
    try:
        cv2.imwrite(filename, image_matrix)
        return True
    except Exception:
        print("A imagem nao foi salva!")
        return False


def rotateImage(imgMatrix, rotAngle):
    """

    :param imgMatrix: A list of ints with the matrix of pixels of the image
    :param rotAngle: Image rotation angle
    :return: rotated: A list of ints with the matrix of pixels of the image

    """
    try:
        #   pega a altura e largura da imagem
        height, width = imgMatrix.shape[:2]

        #   pega o ponto central da imagem
        centralPoint = (width / 2, height / 2)

        #   obtem uma matriz de rotacao com base no ponto central dado e no angulo fornecido
        rotation = cv2.getRotationMatrix2D(centralPoint, rotAngle, 1.0)
        rotated = cv2.warpAffine(imgMatrix, rotation, (width, height))
    except Exception as e:
        return np.array([])

    #   retorna a matrix da imagem rotacionada
    return rotated
