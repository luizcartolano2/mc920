__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "Finished"
__version__ = "2.0"
__date__    = "16 april 2019"


######################
#   SETA O LOGGER    #
######################
import logger_lib
logger = logger_lib.get_logger('basicImage')


try:
    import cv2
    import numpy as np
    from scipy import signal, ndimage
    from matplotlib.pylab import imshow, show
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
        image_matrix = cv2.imread(filename, 0)
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

    logger.info('Imagem ' + str(filename) + ' teve seus planos separados com sucesso.')
    return plane.astype('uint8')


def convert_255_to_1(img, filename='Nao informado!'):
    """

    :param img: The image matrix in [0, 255]
    :param filename: The filename of the image that will be managed
    :return: The image matrix in [0, 1]

    """
    try:
        logger.info('Conversao da imagem de [0, 255] para [0, 1] feita com sucesso!')
        return cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
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
        # img = img * 255
        img = cv2.normalize(img,  None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        logger.info('Imagem ' + str(filename) + ' convertida com sucesso para [0, 255].')
        return img
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

    logger.info('Imagem ' + str(filename) + ' teve seu brilho ajustado com sucesso.')
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
        logger.info('Imagems ' + str(filename1) + 'e ' + str(filename2)+ ' combinadas com sucesso.')
        return image
    else:
        logger.error('Nao foi possivel aplicar a tecnica para as imagens - ' + str(filename1) + ' e ' + str(filename2) +                                                                             ' pois elas possuem dimensoes diferentes.')
        return np.array([])


def puzzle_image(img, num_split, filename='Nao informado!'):
    """

    :param img: A list of ints with the matrix of pixels of the image
    :param num_split: Number of rows the image will be split
    :param filename: The filename of the image that will be managed
    :return: A list with the image splited in squares of same size

    """
    # first we must make sure that the image has the same x and y dimensions
    if img.shape[0] == img.shape[1] and num_split != 0:
        # then we check if divisors fit to image dimensions
        if img.shape[0] % num_split == 0:
            try:
                # here we clone the image
                img_clone = img.copy()
            except Exception as e:
                logger.error('Problemas ao clonar a imagem(' + str(filename) + '! Erro: ' + str(e))
                return []
            x = y = 0
            image_vector = [None] * (num_split ** 2)
            num_squares = 0
            while y < img.shape[1]:
                while x < img.shape[0]:
                    try:
                        image_vector[num_squares] = img_clone[int(y):int(y+(img.shape[1]/num_split)), int(x):int(x+(img.shape[0]/num_split))]
                    except Exception as e:
                        logger.error('Problemas ao splitar a imagem(' + str(filename) + '! Erro: ' + str(e))
                        return []
                    x = x + img.shape[1] / num_split
                    num_squares = num_squares + 1
                x = 0
                y = y + img.shape[1]/num_split

            logger.info('Imagem ' + str(filename) + ' dividida com sucesso.')
            return image_vector
        else:
            logger.info('Nao foi possivel dividir a imagem(' + str(filename) + ' pois o tamanho da imagem nao e multiplo do numero de divisoes.')
            return []
    else:
        logger.info('Nao foi possivel dividir a image(' + str(filename) + ' pois ela nao possue as mesmas dimensoes para X e Y!')
        return []


def combine_images_4x4(img_list, img_order, filename='Nao informado!'):
    """

    :param img_list: List whith the squares of the original image
    :param img_order: List with the new order the image will receive
    :param filename: Filename of the original image
    :return: np.array with the recombined image

    """
    if len(img_list) > 0:
        if len(img_order) == 16:
            try:
                hor1 = np.hstack((img_list[img_order[0] - 1], img_list[img_order[1] - 1], img_list[img_order[2] - 1], img_list[img_order[3] - 1]))
                hor2 = np.hstack((img_list[img_order[4] - 1], img_list[img_order[5] - 1], img_list[img_order[6] - 1], img_list[img_order[7] - 1]))
                hor3 = np.hstack((img_list[img_order[8] - 1], img_list[img_order[9] - 1], img_list[img_order[10] - 1], img_list[img_order[11] - 1]))
                hor4 = np.hstack((img_list[img_order[12] - 1], img_list[img_order[13] - 1], img_list[img_order[14] - 1], img_list[img_order[15] - 1]))
            except Exception as e:
                logger.error('Problemas ao juntar horizontalmete a imagem(' + str(filename) + '): ' + str(e))
                return np.array([])

            try:
                vertical_image = np.vstack((hor1, hor2, hor3, hor4))
                logger.info('Imagem ' + str(filename) + ' recombinada com sucesso.')
                return vertical_image
            except Exception as e:
                logger.error('Problemas ao juntar verticalmente a imagem(' + str(filename) + '): ' + str(e))
                return np.array([])
        else:
            logger.info('A funcao para recombinar as imagens nao pode ser executada para a imagem: ' + str(filename) +
                        ' pois nao foi fornecida uma ordem correta para recombinacao.')
            return np.array([])

    else:
        logger.info('A funcao para recombinar as imagens nao pode ser executada para a imagem: ' + str(filename) +
                     ' pois nao foi fornecida uma lista valida de imagens.')
        return np.array([])


def space_filter(img, filename='Nao informado!'):
    """

    :param img: A list of ints with the matrix of pixels of the image
    :param filename: filename of the image
    :return: the images with the filter applied

    """
    matrix_1 = np.array([[0., 0., -1., 0., 0.],[0., -1., -2., -1., 0.],[-1., -2., 16., -2., -1.],[0., -1., -2., -1., 0.],[0., 0., -1., 0., 0.]])
    try:
        # primeiro filtro
        filter_1 = cv2.filter2D(img, -1, matrix_1)
        logger.info('Imagem ' + str(filename) + ' teve o filtro h1 aplicado com sucesso.')
    except Exception as e:
        filter_1 = np.array([])
        logger.error('Erro ao aplicar a funcao h1 a imagem - ' + str(filename) + ' pois: ' + str(e))

    matrix_2 = np.array([[1., 4., 6., 4., 1.],[4., 16., 24., 16., 4.],[6., 24., 36., 24., 6.],[4., 16., 24., 16., 4.],[1., 4., 6., 4., 1.]])/256
    try:
        # segundo filtro
        filter_2 = cv2.filter2D(img, -1, matrix_2)
        logger.info('Imagem ' + str(filename) + ' teve o filtro h2 aplicado com sucesso.')
    except Exception as e:
        filter_2 = np.array([])
        logger.error('Erro ao aplicar a funcao h2 a imagem - ' + str(filename) + ' pois: ' + str(e))

    matrix_3 = np.array([[-1., 0., 1.],[-2., 0., 2.],[-1., 0., 1.]])
    try:
        # terceiro filtro
        filter_3 = cv2.filter2D(img, -1, matrix_3)
        logger.info('Imagem ' + str(filename) + ' teve o filtro h3 aplicado com sucesso.')
    except Exception as e:
        filter_3 = np.array([])
        logger.error('Erro ao aplicar a funcao h3 a imagem - ' + str(filename) + ' pois: ' + str(e))

    matrix_4 = np.array([[-1., -2., -1.],[0., 0., 0.],[1., 2., 1.]])
    try:
        # quarto filtro
        filter_4 = cv2.filter2D(img, -1, matrix_4)
        logger.info('Imagem ' + str(filename) + ' teve o filtro h4 aplicado com sucesso.')
    except Exception as e:
        filter_4 = np.array([])
        logger.error('Erro ao aplicar a funcao h4 a imagem - ' + str(filename) + ' pois: ' + str(e))

    try:
        # mistura dos filtros 3 e 4
        #  a formula para combinar as matrizes eh dada por sqrt(h3^2 + h4^2)
        filter_3_4 = np.sqrt(np.add(np.square(filter_3.astype(np.float32)),np.square(filter_4.astype(np.float32))))

        logger.info('Imagem ' + str(filename) + ' teve os filtro h3/h4 aplicados com sucesso.')
    except Exception as e:
        filter_3_4 = np.array([])
        logger.error('Erro ao aplicar a funcao h3/h4 a imagem - ' + str(filename) + ' pois: ' + str(e))

    return filter_1.astype(np.uint8), filter_2.astype(np.uint8), filter_3.astype(np.uint8), filter_4.astype(np.uint8), filter_3_4.astype(np.uint8)


def gaussian_blur(img, filename='Nao informado!'):
    """

    :param img: A list of ints with the matrix of pixels of the image
    :param filename: filename of the image
    :return: a list of images with the filter applied

    """
    outputs = []
    for i in range(1,10,2):

        try:
            # cria o filtro gaussiano
            kernel = np.outer(cv2.getGaussianKernel(ksize=11,sigma=i),cv2.getGaussianKernel(ksize=11,sigma=i))
        except Exception as e:
            outputs.append(np.array([]))
            logger.error('Erro ao criar o kernel gaussiano para a imagem - ' + str(filename) + ' pois: ' + str(e))
            continue

        try:
            # chama a funcao que ira realizar a convolucao pelo metodo das transformadas de fourier
            blurred = signal.fftconvolve(img, kernel, mode='same')
        except Exception as e:
            outputs.append(np.array([]))
            logger.error('Erro ao realizar a convolucao da imagem - ' + str(filename) + ' pois: ' + str(e))
            continue

        try:
            # converte para escala logaritmica
            ones = np.ones(blurred.shape, blurred.dtype)
            out_image = np.log(blurred + ones)
        except Exception as e:
            outputs.append(np.array([]))
            logger.error('Erro na transformacao logaritmica da imagem - ' + str(filename) + ' pois: ' + str(e))
            continue

        try:
            # normaliza a imagem para poder ser visualizada
            out_image = convert_1_to_255(out_image, filename)
        except Exception as e:
            outputs.append(np.array([]))
            logger.error('Erro na normalizacao da imagem - ' + str(filename) + ' pois: ' + str(e))
            continue

        storage_gaussian_kernal(kernel, 'frequencia/gaussiana/gaussiana-' + str(i))

        # adiciona a imagem a lista de saída
        logger.info('Imagem ' + str(filename) + ' teve o kernel gaussiano ' + str(i) + ' aplicados com sucesso.')
        outputs.append(out_image)

    return outputs


def storage_gaussian_kernal(img, name):
    """

    :param img: A list of ints with the matrix of pixels of the image
    :param name: filename of the image
    :return: ---

    """
    try:
        fft = np.fft.fft2(img)
        fft_shift = np.fft.fftshift(fft)
        mag_spectrum = 20*np.log(np.abs(fft_shift)+1)
    except:
        return False
    try:
        magnitude_spectrum = convert_1_to_255(mag_spectrum)
        store_image('outputs/' + str(name) + '.png', magnitude_spectrum)
        return True
    except:
        return False


def gaussian_blur_implemented(img, filename=None):
    """

    :param img: A list of ints with the matrix of pixels of the image
    :param filename: filename of the image
    :return: a list of images with the filter applied

    """
    outputs = []
    for i in range(1, 10, 2):

        try:
            # aplica fourier na imagem
            fft = np.fft.fft2(img)
            fft_shift = np.fft.fftshift(fft)
        except Exception as e:
            outputs.append(np.array([]))
            logger.error('Erro ao aplicar fourier na imagem - ' + str(filename) + ' pois: ' + str(e))
            continue

        try:
            # cria o kernel
            kernel = cv2.getGaussianKernel(ksize=11, sigma=i)
            kernel = kernel * kernel.T
            kernel_fft = np.fft.fft2(kernel, img.shape)
            kernel_fft_shift = np.fft.fftshift(kernel_fft)
        except Exception as e:
            outputs.append(np.array([]))
            logger.error('Erro ao criar o kernel gaussiano para a imagem - ' + str(filename) + ' pois: ' + str(e))
            continue

        try:
            # multiplica a imagem e a matriz
            blurred = fft_shift * kernel_fft_shift
        except Exception as e:
            outputs.append(np.array([]))
            logger.error('Erro ao multiplicar as matrizes para a imagem - ' + str(filename) + ' pois: ' + str(e))
            continue

        try:
            # faz um unshift da imagem
            f_ishift = np.fft.ifftshift(blurred)
            img_back = np.fft.ifft2(f_ishift)
        except Exception as e:
            outputs.append(np.array([]))
            logger.error('Erro ao voltar a imagem - ' + str(filename) + ' pois: ' + str(e))
            continue

        try:
            # normaliza a imagem
            img_back = np.abs(img_back)
            img_back = convert_1_to_255(img_back)
        except Exception as e:
            outputs.append(np.array([]))
            logger.error('Erro ao normalizar a imagem - ' + str(filename) + ' pois: ' + str(e))
            continue

        try:
            storage_gaussian_kernal(kernel, 'frequencia-2/gaussiana-2/gaussiana-' + str(i))
            storage_gaussian_kernal(img, 'frequencia-2/spectro/espectro-' + str(filename[0:-4]))
            storage_gaussian_kernal(img_back, 'frequencia-2/spectro/espectro-saida-' + str(filename[0:-4]))
        except Exception:
            pass

        outputs.append(img_back)

    return outputs
