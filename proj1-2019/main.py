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
    tempos_scipy = []
    tempos_normal = []

    image = read_image(IMAGE_PATH + '/' + 'baboon.png')

    for i in range(0,200):
        start = time.time()
        res = gaussian_blur(image, 'baboon.png')
        end = time.time()
        tempos_scipy.append(end - start)

    for i in range(0,200):
        start = time.time()
        res = gaussian_blur_implemented(image, 'baboon.png')
        end = time.time()
        tempos_normal.append(end - start)

    # tempo da implementacao manual
    media_normal = mean(tempos_normal)
    desvio_normal = stdev(tempos_normal)
    intervalo_conf_normal = '(' + str(media_normal - 1.96 * (desvio_normal / (len(tempos_normal)) ** (1 / 2))) + ',' + str(
        media_normal + 1.96 * (desvio_normal / (len(tempos_normal)) ** (1 / 2))) + ')'
    print("Media do tempo gasto para a busca DFS: " + str(media_normal))
    print("Desvio padrao do tempo gasto para a busca DFS: " + str(desvio_normal))
    print("Intervalo de confiança para a busca DFS: " + intervalo_conf_normal)
    fig = plt.figure()
    plt.hist(tempos_normal, bins=10)
    plt.show()

    # tempo da implementacao sicpy
    media_s = mean(tempos_scipy)
    desvio_s = stdev(tempos_scipy)
    intervalo_conf_s = '(' + str(media_s - 1.96 * (desvio_s / (len(tempos_normal)) ** (1 / 2))) + ',' + str(
        media_s + 1.96 * (desvio_s / (len(tempos_normal)) ** (1 / 2))) + ')'
    print("Media do tempo gasto para a busca DFS: " + str(media_s))
    print("Desvio padrao do tempo gasto para a busca DFS: " + str(desvio_normal))
    print("Intervalo de confiança para a busca DFS: " + intervalo_conf_s)
    fig = plt.figure()
    plt.hist(tempos_scipy, bins=10)
    plt.show()

    pdb.set_trace()

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

    # loop para executar o filtro espacial sobre todas as imagens
    for image in images:
        h1, h2, h3, h4, h5 = space_filter(image[0], image[1])
        store_image('outputs/espacial/filter_h1/h1_' + str(image[1]), h1)
        store_image('outputs/espacial/filter_h2/h2_' + str(image[1]), h2)
        store_image('outputs/espacial/filter_h3/h3_' + str(image[1]), h3)
        store_image('outputs/espacial/filter_h4/h4_' + str(image[1]), h4)
        store_image('outputs/espacial/filter_h3_h4/h3_h4_' + str(image[1]), h5)

    # loop para executar o filtro gaussiano sobre todas as imagens
    for image in images:
        res = gaussian_blur(image[0], image[1])
        store_image('outputs/frequencia/sigma-1/s1-' + str(image[1]), res[0])
        store_image('outputs/frequencia/sigma-3/s3-' + str(image[1]), res[1])
        store_image('outputs/frequencia/sigma-5/s5-' + str(image[1]), res[2])
        store_image('outputs/frequencia/sigma-7/s7-' + str(image[1]), res[3])
        store_image('outputs/frequencia/sigma-9/s9-' + str(image[1]), res[4])

    # loop para executar o filtro gaussiano sobre todas as imagens
    for image in images:
        res = gaussian_blur_implemented(image[0], image[1])
        store_image('outputs/frequencia-2/sigma-1/s1-' + str(image[1]), res[0])
        store_image('outputs/frequencia-2/sigma-3/s3-' + str(image[1]), res[1])
        store_image('outputs/frequencia-2/sigma-5/s5-' + str(image[1]), res[2])
        store_image('outputs/frequencia-2/sigma-7/s7-' + str(image[1]), res[3])
        store_image('outputs/frequencia-2/sigma-9/s9-' + str(image[1]), res[4])

if __name__ == '__main__':
    logger.info("Path para o projeto: " + str(PROJ_PATH))
    logger.info("Path para o diretorio : " + str(WKS_PATH))
    logger.info("Path para a pasta com as imagens: " + str(IMAGE_PATH))
    logger.info("Path para a pasta que ira salvar os outputs: " + str(OUTPUT_PATH))

    #   essa linha apaga tudo que foi escrito no terminal ate o momento, ela nao funciona no pycharm
    # os.system('cls' if os.name == 'nt' else 'clear')

    main()
