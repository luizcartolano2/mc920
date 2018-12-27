from importer import install
import logging

logger = logging.getLogger('log_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

packages = ['numpy', 'opencv-python', 'scikit-image']
for pack in packages:
    if install(pack):
        logger.debug("Pacote: " + pack + " instalado corretamente.")
    else:
        logger.debug("Problemas para instalar o pacote " + pack)

import os
import threading

# paths para a pasta
PROJ_PATH = os.getcwd()
WKS_PATH = os.path.abspath(os.path.join(PROJ_PATH, os.pardir))
IMAGE_PATH = WKS_PATH + '/images/'
OUTPUT_PATH = PROJ_PATH + '/output/'


def main():
    pass


if __name__ == '__main__':

    logger.debug("Path para o projeto: " + PROJ_PATH)
    logger.debug("Path para o diretorio: " + WKS_PATH)
    logger.debug("Path para a pasta com as imagens: " + IMAGE_PATH)
    logger.debug("Path para a pasta que ira salvar os outputs: " + OUTPUT_PATH)

    #   essa linha apaga tudo que foi escrito no terminal ate o momento, ela nao funciona no pycharm
    # os.system('cls' if os.name == 'nt' else 'clear')

    main()
