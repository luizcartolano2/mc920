__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "production"
__version__ = "1.0"
__date__    = ""


######################
#   SETA O LOGGER    #
######################
import logger_lib
logger = logger_lib.get_logger('basicImage')


try:
    import cv2
    import numpy as np
    from matplotlib.pyplot import imshow, show
except ImportError as e:
    logger.error('Problemas ao importar: ' + str(e))
    raise SystemExit(1)


def read_image(filename):
    """
    Method to read new images

    :param filename: The file location of the image
    :return: img: A list of ints with the matrix of pixels of the image

    """
    #   read the image
    try:
        image_matrix = cv2.imread(filename, 1)
        img = image_matrix.astype(dtype='uint8')
        logger.info('Imagem ' + str(filename) + ' lida com sucesso.')
    except Exception as e:
        logger.error('Imagem' + str(filename) + ' nao foi lida pois ' + str(e))
        return np.array([])

    #   return the image readed
    return img


def store_image(filename, image_matrix):
    """
    Method to store new images

    :param filename: The file location of the image
    :param image_matrix: A list of ints with the matrix of pixels of the image
    :return: None

    """
    try:
        cv2.imwrite(filename, image_matrix)
        logger.info('Imagem ' + str(filename) + ' salva com sucesso.')
        return True
    except Exception as e:
        logger.error('Imagem' + str(filename) + ' nao foi salva pois ' + str(e))
        return False


def write_plans(img, img_plane):
    """

        Method to show specific planes of the image

        Parameters
        ----------
            img : list
                A list of ints with the matrix of pixels of the image

            img_plane : int
                The plane the code will show

        Returns
        -------
            Nothing
    
    """
    try:
        plane = np.empty(img.shape)
    except Exception as e:
        logger.error('Erro ao criar um plano vazio: ' + str(e))
        return False

    try:
        plane[:, :, 2] = ((img[:, :, 2] >> img_plane) % 2) * 255
        plane[:, :, 1] = ((img[:, :, 1] >> img_plane) % 2) * 255
        plane[:, :, 0] = ((img[:, :, 0] >> img_plane) % 2) * 255
    except Exception as e:
        logger.error('Erro ao associar o plano especificado ao plano vazio anteriormente criado: ' + str(e))
        return False

    imshow(plane)
    show()

    return True


def convert_255_to_1(img):
    """

    :param img: The image matrix in [0, 255]
    :return: The image matrix in [0, 1]

    """
    return img/255
    # return cv2.normalize(img, None, alpha = 0, beta = 1, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)


def convert_1_to_255(img):
    """

    :param img: The image matrix in [0, 1]
    :return: The image matrix in [0, 255]

    """
    img = img * 255
    return img.astype('uint8')
    # return cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)


def adjust_brightness(img, gama):
    """

    :param img:
    :param gama:
    :return:

    """
    image = convert_255_to_1(img)
    image = image ** (1/gama)

    return convert_1_to_255(image)