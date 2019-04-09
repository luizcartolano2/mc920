__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "production"
__version__ = "1.0"
__date__    = "24 March 2019"

######################
#   SETA O LOGGER    #
######################
import logger_lib
logger = logger_lib.get_logger('main')

try:
    import os
    import threading
    from importer import install_and_import
    from constants import PROJ_PATH, IMAGE_PATH, OUTPUT_PATH, WKS_PATH
    import pdb
except ImportError as e:
    logger.error('Problemas ao importar: ' + str(e))
    raise SystemExit


################################
#   BAIXA OS PACOTES USADOS    #
################################
# packages = ['numpy', 'opencv-python', 'scikit-image', 'matplotlib']
# for package in packages:
#     if install_and_import(package):
#         logger.info("Pacote: " + package + " instalado corretamente.")
#     else:
#         logger.warning("Problemas para instalar o pacote " + package)


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
            space_filter(image)
            images.append([image, filename])

    for image in images:
        h1, h2, h3, h4, h5 = space_filter(image[0], image[1])
        store_image('outputs/filter_h1/h1_' + str(image[1]), h1)
        store_image('outputs/filter_h2/h2_' + str(image[1]), h2)
        store_image('outputs/filter_h3/h3_' + str(image[1]), h3)
        store_image('outputs/filter_h4/h4_' + str(image[1]), h4)
        store_image('outputs/filter_h3_h4/h3_h4_' + str(image[1]), h5)

if __name__ == '__main__':
    logger.info("Path para o projeto: " + str(PROJ_PATH))
    logger.info("Path para o diretorio : " + str(WKS_PATH))
    logger.info("Path para a pasta com as imagens: " + str(IMAGE_PATH))
    logger.info("Path para a pasta que ira salvar os outputs: " + str(OUTPUT_PATH))

    #   essa linha apaga tudo que foi escrito no terminal ate o momento, ela nao funciona no pycharm
    # os.system('cls' if os.name == 'nt' else 'clear')

    main()
