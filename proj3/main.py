import os
from basicImage import readImage, storeImage, rotateImage
from imageAlign import houghTransform

def main():
    # paths para a pasta
    pathIn = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/imagesInclinadas/'
    pathOutProjHor = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj3/output/projecaoHorizontal/'
    pathOutHough = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj3/output/Hough/'

    # for percorrendo todos os arquivos da pasta de imagens inclinadas e aplicando as tecnicas estudas
    for filename in os.listdir(pathIn):
        print("Trabalhando com o arquivo: " + filename)
        #   conversao da imagem para a matrix que a representa
        print("\tLendo a imagem:")
        imageMatrix = readImage(pathIn+filename)

        #   aplica a tecnica da projecao horizontal
        # print("\tAplicando a tecnica da projecao Horizontal:")
        
        # print("\t\tAngulo calculado pela projecao Horizontal: ")
        
        #   aplica a tecnica da transformada de Hough
        print("\tAplicando a tecnica da transformada de Hough:")
        #   pega o angulo a ser transformado
        houghAngle = houghTransform(imageMatrix)
        print("\t\tAngulo calculado pela transformada de Hough: " + str(houghAngle))

        #   salva a imagem pos projecao Horizontal
        print("\tSalvando imagem apos aplicacao da projecao Horizontal: ")

        #   salva a imagem pos transformada de Hough
        print("\tSalvando imagem apos aplicacao da transformada de Hough: ")
        #   aplica a rotacao
        houghImage = rotateImage(imageMatrix,houghAngle)
        #   salva a imagem rotacionada
        storeImage(pathOutHough+filename, houghImage)

        #   quebra de linha entre os itens que estao sendo iterados
        print("\n")

    

if __name__ == '__main__':
    main()
