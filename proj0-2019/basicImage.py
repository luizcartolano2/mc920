__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "production"
__version__ = "1.0"
__date__    = "14 March 2019"


######################
#   SETA O LOGGER    #
######################
import logger_lib
logger = logger_lib.get_logger('basicImage')


try:
    import cv2
    import numpy as np
    import pdb
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


def write_plans(img, img_plane, filename='Nao informado!'):
    """

    :param img: A list of ints with the matrix of pixels of the image
    :param img_plane: The plane the code will show
    :param filename: The filename of the image that will be managed
    :return:

    """
    try:
        plane = np.empty(img.shape)
    except Exception as e:
        logger.error('Erro ao criar um plano vazio: ' + str(e) + ' para a imagem: ' + str(filename))
        return np.array([])

    try:
        plane[:, :, 2] = ((img[:, :, 2] >> img_plane) % 2) * 255
        plane[:, :, 1] = ((img[:, :, 1] >> img_plane) % 2) * 255
        plane[:, :, 0] = ((img[:, :, 0] >> img_plane) % 2) * 255
    except Exception as e:
        logger.error('Erro ao associar o plano especificado ao plano vazio anteriormente criado: ' + str(e) + ' para a imagem: ' + str(filename))
        return np.array([])

    return plane.astype('uint8')


def convert_255_to_1(img, filename='Nao informado!'):
    """

    :param img: The image matrix in [0, 255]
    :param filename: The filename of the image that will be managed
    :return: The image matrix in [0, 1]

    """
    try:
        logger.info('Conversao da imagem de [0, 255] para [0, 1] feita com sucesso!')
        return img/255
    except Exception as e:
        logger.error('Problemas ao converter a imagem(' + str(filename) + ') de [0, 255] para [0, 1]: ' + str(e))
        return np.array([])


def convert_1_to_255(img, filename='Nao informado!'):
    """

    :param img: The image matrix in [0, 1]
    :param filename: The filename of the image that will be managed
    :return: The image matrix in [0, 255]

    """
    try:
        img = img * 255
        return img.astype('uint8')
    except Exception as e:
        logger.error('Problemas ao converter a imagem(' + str(filename) + ') de [0, 1] para [0, 255]: ' + str(e))
        return np.array([])


def adjust_brightness(img, gama, filename='Nao informado!'):
    """

    :param img: A list of ints with the matrix of pixels of the image
    :param gama: The brightness factor
    :param filename: The filename of the image that will be managed
    :return: A list of ints with the matrix of pixels of the image after the function

    """

    image = convert_255_to_1(img)
    if image.size == 0:
        logger.error('Erro ao aplicar a funcao adjust_brightness a image - ' + str(filename))
        return np.array([])

    try:
        image = image ** (1/gama)
    except Exception as e:
        logger.error('Erro ao aplicar a funcao gama a imagem(' + str(filename) + '): ' + str(e))
        return np.array([])

    image = convert_1_to_255(image)
    if image.size == 0:
        logger.error('Erro ao aplicar a funcao adjust_brightness a image - ' + str(filename))
        return np.array([])

    return image


def merge_weighted_average(img1, weight1, img2, weight2, filename1='Nao informado!', filename2='Nao informado!'):
    """

    :param img1: A list of ints with the matrix of pixels of the first image
    :param weight1: The weight the first image will have in the final result
    :param img2: A list of ints with the matrix of pixels of the second image
    :param weight2: The weight the second image will have in the final result
    :param filename1: The filename1 of the image that will be managed
    :param filename2: The filename2 of the image that will be managed
    :return: The final image that is the two images combined in a weighted average strategy

    """
    if img1.size == img2.size:
        try:
            image = weight1 * img1 + weight2 * img2
        except Exception as e:
            logger.error('Falha ao operar com os arrays: ' + str(e) + ' nas imagens: ' + str(filename1) + ' e ' + str(filename2))
            return np.array([])
        return image
    else:
        logger.error('Nao foi possivel aplicar a tecnica para as imagens - ' + str(filename1) + ' e ' + str(filename2) +
                                                                             ' pois elas possuem dimensoes diferentes.')
        return np.array([])


def puzzle_image(img, num_split, filename='Nao informado!'):
    """

    :param img: A list of ints with the matrix of pixels of the image
    :param num_split: Number of rows the image will be split
    :param filename: The filename of the image that will be managed
    :return: A list with the image splited in squares of same size

    """
    # first we must make sure that the image has the same x and y dimensions
    if img.shape[0] == img.shape[1]:
        # then we check if divisors fit to image dimensions
        if img.shape[0] % num_split == 0:
            # here we clone the image
            img_clone = img.copy()
            x = y = 0
            image_vector = [None] * (num_split ** 2)
            num_squares = 0
            while y < img.shape[1]:
                while x < img.shape[0]:
                    image_vector[num_squares] = img_clone[int(y):int(y+(img.shape[1]/num_split)), int(x):int(x+(img.shape[0]/num_split))]
                    x = x + img.shape[1] / num_split
                    num_squares = num_squares + 1
                x = 0
                y = y + img.shape[1]/num_split

            return image_vector
        else:
            logger.info('Nao foi possivel dividir a image(' + str(filename) + ' pois o tamanho da imagem nao e multiplo do numero de divisoes.')
            return []
    else:
        logger.info('Nao foi possivel dividir a image(' + str(filename) + ' pois ela nao possue as mesmas dimensoes para X e Y!')
        return []
