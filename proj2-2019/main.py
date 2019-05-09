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


def teste_processamento():
    tempos_3 = []
    tempos_4 = []
    tempo_floyd = []

    image = read_image(IMAGE_PATH + '/' + 'baboon.png')

    for i in range(0,1000):
        start = time.time()
        res = halftoning_3x3(image, 'baboon.png')
        end = time.time()
        tempos_3.append(end - start)

    for i in range(0,1000):
        start = time.time()
        res = halftoning_4x4(image, 'baboon.png')
        end = time.time()
        tempos_4.append(end - start)

    for i in range(0,1000):
        start = time.time()
        res = floyd_steinberg(image, 'baboon.png')
        end = time.time()
        tempo_floyd.append(end - start)

    for lst in [tempos_3, tempos_4, tempo_floyd]:
        # tempo da implementacao manual
        media_normal = mean(lst)
        desvio_normal = stdev(lst)
        intervalo_conf_normal = '(' + str(media_normal - 1.96 * (desvio_normal / (len(lst)) ** (1 / 2))) + ',' + str(
            media_normal + 1.96 * (desvio_normal / (len(lst)) ** (1 / 2))) + ')'
        print("-----------------------------------------------------------------------------------------------------------------")
        print("| Media do tempo gasto para a busca DFS: " + str(media_normal))
        print("| Desvio padrao do tempo gasto para a busca DFS: " + str(desvio_normal))
        print("| Intervalo de confiança para a busca DFS: " + intervalo_conf_normal)
        print("-----------------------------------------------------------------------------------------------------------------")


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

    for image in images:
        filename = image[1][0:image[1].find('.')] + '.pbm'
        store_image(OUTPUT_PATH + 'ordenado/matriz3/' + filename, halftoning_3x3(image[0], filename))
        store_image(OUTPUT_PATH + 'ordenado/matriz4/' + filename, halftoning_4x4(image[0], filename))

    for image in images:
        filename = image[1][0:image[1].find('.')] + '.pbm'
        store_image(OUTPUT_PATH + 'nao-ordenado/' + filename, floyd_steinberg(image[0], filename))

if __name__ == '__main__':
    logger.info("Path para o projeto: " + str(PROJ_PATH))
    logger.info("Path para o diretorio : " + str(WKS_PATH))
    logger.info("Path para a pasta com as imagens: " + str(IMAGE_PATH))
    logger.info("Path para a pasta que ira salvar os outputs: " + str(OUTPUT_PATH))

    #   essa linha apaga tudo que foi escrito no terminal ate o momento, ela nao funciona no pycharm
    # os.system('cls' if os.name == 'nt' else 'clear')
    # teste_processamento()
    main()
