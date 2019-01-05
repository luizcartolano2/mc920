import logging
import os
import threading
from importer import install
from constants import PROJ_PATH, IMAGE_PATH, OUTPUT_PATH, WKS_PATH

######################
#   SETA O LOGGER    #
######################
logger = logging.getLogger('log_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

################################
#   BAIXA OS PACOTES USADOS    #
################################
packages = ['numpy', 'opencv-python', 'scikit-image']
for package in packages:
    if install(package):
        logger.debug("Pacote: " + package + " instalado corretamente.")
    else:
        logger.debug("Problemas para instalar o pacote " + package)


#   importa as funcoes dos demais arquivos
from basicImage import readImage, storeImage


def main():
    """

    :return:

    """
    pass


if __name__ == '__main__':

    logger.debug("Path para o projeto: " + PROJ_PATH)
    logger.debug("Path para o diretorio : " + WKS_PATH)
    logger.debug("Path para a pasta com as imagens: " + IMAGE_PATH)
    logger.debug("Path para a pasta que ira salvar os outputs: " + OUTPUT_PATH)

    #   essa linha apaga tudo que foi escrito no terminal ate o momento, ela nao funciona no pycharm
    # os.system('cls' if os.name == 'nt' else 'clear')

    main()
