from importer import install
from constants import pathIn, pathOutProjHor, pathOutHough
import logging
import os
import threading

######################
#   SETA O LOGGER    #
######################
logger = logging.getLogger('server_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

################################
#   BAIXA OS PACOTES USADOS    #
################################
packages = ['numpy', 'opencv-python', 'scikit-image']
for pack in packages:
    if install(pack):
        logger.info("Pacote: " + pack + " instalado corretamente.")
    else:
        logger.warning("Problemas para instalar o pacote " + pack)

from basicImage import readImage, storeImage, rotateImage
from imageAlign import houghTransform, horizontalProjection


def alignImage(filename):
    """

    :param filename:
    :return:

    """
    print("Trabalhando com o arquivo: " + filename)
    ##########################
    #   LEITURA DA IMAGEM    #
    ##########################
    #   conversao da imagem para a matrix que a representa
    print("\tLendo a imagem:")
    imageMatrix = readImage(pathIn + filename)
    if imageMatrix.size == 0:
        logger.warning(filename + ' nao foi lido corretamente!')
        return
    else:
        logger.info(filename + ' lido corretamente!')

    ##################################
    #   APLICA TECNICAS DE ROTACAO   #
    ##################################
    #   tecnica da projecao horizontal
    print("\tAplicando a tecnica da projecao Horizontal:")
    projAngle = horizontalProjection(imageMatrix)
    if projAngle is None:
        logger.warning(filename + " falha ao aplicar a tecnica da projecao horizontal.")
        return
    logger.info("Angulo calculado pela projecao Horizontal: " + str(projAngle) + " para o arquivo: " + filename)

    #   tecnica da transformada de Hough
    print("\tAplicando a tecnica da transformada de Hough:")
    #   pega o angulo a ser transformado
    houghAngle = houghTransform(imageMatrix)
    if houghAngle is None:
        logger.warning(filename + " falha ao aplicar a tecnica da transformada de hough.")
        return
    logger.info("Angulo calculado pela transformada de Hough: " + str(houghAngle) + " para o arquivo: " + filename)

    ############################
    #   ROTACIONA AS IMAGENS   #
    ############################
    #   salva a imagem pos projecao Horizontal
    print("\tSalvando imagem apos aplicacao da projecao Horizontal: ")
    projImage = rotateImage(imageMatrix, projAngle)
    if projImage.size == 0:
        logger.warning(filename + ' nao foi rotacionado corretamente pela projecao horizontal.')
        return
    else:
        logger.info(filename + ' rotacionado corretamente pela projecao horizontal.')

    #   salva a imagem pos transformada de Hough
    print("\tSalvando imagem apos aplicacao da transformada de Hough: ")
    houghImage = rotateImage(imageMatrix, houghAngle)
    if houghImage.size == 0:
        logger.warning(filename + ' nao foi rotacionado corretamente pela transformacao de Hough.')
        return
    else:
        logger.info(filename + ' rotacionado corretamente pela transformacao de Hough.')

    #####################################
    #   SALVA AS IMAGENS ROTACIONADAS   #
    #####################################
    #   salva a imagem rotacionada pela projecao horizontal
    if not storeImage(pathOutProjHor + filename, projImage):
        logger.warning(filename + " nao foi salvo corretamente apos aplicacao da projecao horizontal.")
    else:
        logger.info(filename + " salvo corretamente apos aplicacao da projecao horizontal.")

    #   salva a imagem rotacionada pela transformada de Hough
    if not storeImage(pathOutHough + filename, houghImage):
        logger.warning(filename + " nao foi salvo corretamente apos aplicacao da transformada de Hough.")
    else:
        logger.info(filename + " salvo corretamente apos aplicacao da transformada de Hough.")

    #   quebra de linha entre os itens que estao sendo iterados
    print("\n")


def main():
    """

    :return:

    """
    files = []
    threads = []

    for filename in os.listdir(pathIn):
        files.append(filename)

    for i in range(len(files)):
        t = threading.Thread(target=alignImage, args=(files[i], ))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
