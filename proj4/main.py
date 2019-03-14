__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "production"
__version__ = "1.0"
__date__    = "16 february 2019"

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
except ImportError as e:
    logger.error('Problemas ao importar: ' + str(e))
    raise SystemExit


################################
#   BAIXA OS PACOTES USADOS    #
################################
packages = ['numpy', 'opencv-python', 'scikit-image']
for package in packages:
    if install_and_import(package):
        logger.info("Pacote: " + package + " instalado corretamente.")
    else:
        logger.warning("Problemas para instalar o pacote " + package)


#   importa as funcoes dos demais arquivos
try:
    from basicImage import readImage, storeImage
except ImportError as e:
    logger.error('Problemas ao importar: ' + str(e))
    raise SystemExit


def main():
    """

    :return:

    """
    pass


if __name__ == '__main__':
    logger.info("Path para o projeto: " + str(PROJ_PATH))
    logger.info("Path para o diretorio : " + str(WKS_PATH))
    logger.info("Path para a pasta com as imagens: " + str(IMAGE_PATH))
    logger.info("Path para a pasta que ira salvar os outputs: " + str(OUTPUT_PATH))

    #   essa linha apaga tudo que foi escrito no terminal ate o momento, ela nao funciona no pycharm
    # os.system('cls' if os.name == 'nt' else 'clear')

    main()
