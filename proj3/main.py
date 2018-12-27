from importer import install
import logging
logging.basicConfig(filename='/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj3/log.log',
                    level=logging.DEBUG)

packages = ['numpy', 'opencv-python', 'scikit-image']
for pack in packages:
    if install(pack):
        logging.info("Pacote: " + pack + " instalado corretamente.")
    else:
        logging.warning("Problemas para instalar o pacote " + pack)

import os
from basicImage import readImage, storeImage, rotateImage
from imageAlign import houghTransform, horizontalProjection
import threading

# paths para a pasta
pathIn = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/imagesInclinadas/'
pathOutProjHor = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj3/output/projecaoHorizontal/'
pathOutHough = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj3/output/Hough/'


def alignImage(filename):

    print("Trabalhando com o arquivo: " + filename)
    ##########################
    #   LEITURA DA IMAGEM    #
    ##########################
    #   conversao da imagem para a matrix que a representa
    print("\tLendo a imagem:")
    imageMatrix = readImage(pathIn + filename)
    if imageMatrix.size == 0:
        logging.warning(filename + ' nao foi lido corretamente!')
        return
    else:
        logging.info(filename + ' lido corretamente!')

    ##################################
    #   APLICA TECNICAS DE ROTACAO   #
    ##################################
    #   tecnica da projecao horizontal
    print("\tAplicando a tecnica da projecao Horizontal:")
    projAngle = horizontalProjection(imageMatrix)
    if projAngle is None:
        logging.warning(filename + " falha ao aplicar a tecnica da projecao horizontal.")
        return
    logging.info("Angulo calculado pela projecao Horizontal: " + str(projAngle) + " para o arquivo: " + filename)

    #   tecnica da transformada de Hough
    print("\tAplicando a tecnica da transformada de Hough:")
    #   pega o angulo a ser transformado
    houghAngle = houghTransform(imageMatrix)
    if houghAngle is None:
        logging.warning(filename + " falha ao aplicar a tecnica da transformada de hough.")
        return
    logging.info("Angulo calculado pela transformada de Hough: " + str(houghAngle) + " para o arquivo: " + filename)

    ############################
    #   ROTACIONA AS IMAGENS   #
    ############################
    #   salva a imagem pos projecao Horizontal
    print("\tSalvando imagem apos aplicacao da projecao Horizontal: ")
    projImage = rotateImage(imageMatrix, projAngle)
    if projImage.size == 0:
        logging.warning(filename + ' nao foi rotacionado corretamente pela projecao horizontal.')
        return
    else:
        logging.info(filename + ' rotacionado corretamente pela projecao horizontal.')

    #   salva a imagem pos transformada de Hough
    print("\tSalvando imagem apos aplicacao da transformada de Hough: ")
    houghImage = rotateImage(imageMatrix, houghAngle)
    if houghImage.size == 0:
        logging.warning(filename + ' nao foi rotacionado corretamente pela transformacao de Hough.')
        return
    else:
        logging.info(filename + ' rotacionado corretamente pela transformacao de Hough.')

    #####################################
    #   SALVA AS IMAGENS ROTACIONADAS   #
    #####################################
    #   salva a imagem rotacionada pela projecao horizontal
    if not storeImage(pathOutProjHor + filename, projImage):
        logging.warning(filename + " nao foi salvo corretamente apos aplicacao da projecao horizontal.")
    else:
        logging.info(filename + " salvo corretamente apos aplicacao da projecao horizontal.")

    #   salva a imagem rotacionada pela transformada de Hough
    if not storeImage(pathOutHough + filename, houghImage):
        logging.warning(filename + " nao foi salvo corretamente apos aplicacao da transformada de Hough.")
    else:
        logging.info(filename + " salvo corretamente apos aplicacao da transformada de Hough.")

    #   quebra de linha entre os itens que estao sendo iterados
    print("\n")


def main():
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
