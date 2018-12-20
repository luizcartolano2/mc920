import os
from basicImage import readImage, storeImage, rotateImage
from imageAlign import houghTransform, horizontalProjection
from importer import install
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
        print("\tNao foi possivel trabalhar com a imagem " + filename)
        return

    ##################################
    #   APLICA TECNICAS DE ROTACAO   #
    ##################################
    #   tecnica da projecao horizontal
    print("\tAplicando a tecnica da projecao Horizontal:")
    projAngle = horizontalProjection(imageMatrix)
    print("\t\tAngulo calculado pela projecao Horizontal: " + str(projAngle))

    #   tecnica da transformada de Hough
    print("\tAplicando a tecnica da transformada de Hough:")
    #   pega o angulo a ser transformado
    houghAngle = houghTransform(imageMatrix)
    print("\t\tAngulo calculado pela transformada de Hough: " + str(houghAngle))

    ############################
    #   ROTACIONA AS IMAGENS   #
    ############################
    #   salva a imagem pos projecao Horizontal
    print("\tSalvando imagem apos aplicacao da projecao Horizontal: ")
    projImage = rotateImage(imageMatrix, projAngle)
    if projImage.size == 0:
        print("\tFalha ao obter a imagem rotacionada!")

    #   salva a imagem pos transformada de Hough
    print("\tSalvando imagem apos aplicacao da transformada de Hough: ")
    houghImage = rotateImage(imageMatrix, houghAngle)
    if houghImage.size == 0:
        print("\tFalha ao obter a imagem rotacionada!")
        return

    #####################################
    #   SALVA AS IMAGENS ROTACIONADAS   #
    #####################################
    #   salva a imagem rotacionada pela projecao horizontal
    storeImage(pathOutProjHor + filename, projImage)

    #   salva a imagem rotacionada pela transformada de Hough
    storeImage(pathOutHough + filename, houghImage)

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
