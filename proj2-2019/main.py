__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "production"
__version__ = "1.0"
__date__    = "09 April 2019"

######################
#   SETA O LOGGER    #
######################
import logger_lib
logger = logger_lib.get_logger('main')

try:
    import os
    import threading
    from constants import PROJ_PATH, IMAGE_PATH, OUTPUT_PATH, WKS_PATH
    import pdb
    import time
    import matplotlib.pyplot as plt
    from statistics import mean, stdev
    import warnings
except ImportError as e:
    logger.error('Problemas ao importar: ' + str(e))
    raise SystemExit

warnings.filterwarnings("ignore")

#   importa as funcoes dos demais arquivos
try:
    from basicImage import *
except ImportError as e:
    logger.error('Problemas ao importar: ' + str(e))
    raise SystemExit(1)


def main():
    """

    :return:

    """
    # loop para ler as imagens e armazenar todas elas em um vetor
    images = []
    for filename in os.listdir(IMAGE_PATH):
        image = read_image(IMAGE_PATH + '/' + filename)
        if image.size == 0:
            pass
        else:
            images.append([image, filename])

    floyd_steinberg(images[0][0])

    for image in images:
        store_image(OUTPUT_PATH + 'ordenado/matriz3/' + image[1], halftoning_3x3(image[0], image[1]))
        store_image(OUTPUT_PATH + 'ordenado/matriz4/' + image[1], halftoning_4x4(image[0], image[1]))

    for image in images:
        store_image(OUTPUT_PATH + 'nao-ordenado/' + image[1], floyd_steinberg(image[0], image[1]))

if __name__ == '__main__':
    logger.info("Path para o projeto: " + str(PROJ_PATH))
    logger.info("Path para o diretorio : " + str(WKS_PATH))
    logger.info("Path para a pasta com as imagens: " + str(IMAGE_PATH))
    logger.info("Path para a pasta que ira salvar os outputs: " + str(OUTPUT_PATH))

    #   essa linha apaga tudo que foi escrito no terminal ate o momento, ela nao funciona no pycharm
    # os.system('cls' if os.name == 'nt' else 'clear')

    main()
