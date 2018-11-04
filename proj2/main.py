import os
from basicImage import readImage, storeImage, writePlans
from basicText import txtToBin, changeNewLine
from esteganografia import encodeImage, decodeImage

def main():
    # path para a pasta
    pathIn = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/colorImages/'
    pathTxt = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/inputTexts/'
    pathOut = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj2/output/'
    
    operation = raw_input("Insert the operation to be made: \n")
    if operation == "codificar":
        print("Codificando a imagem: ")
        #########################################
        #   Leitura dos argumentos de entrada   #
        #########################################
        # input da imagem
        imageInput = raw_input("Insert the input image filename: \n")
        imageInput = pathIn + imageInput

        # input do texto a ser codificado
        txtInput = raw_input("Insert the filename of the text to be inserted: \n")
        txtInput = pathTxt + txtInput

        # plane of the bit will be modify
        bitPlane = input("Insert the bit plane you want to modify: \n")

        # output da imagem
        imageOutput = raw_input("Insert the filename of the output file: \n")
        imageOutput = pathOut + imageOutput

        #########################################
        #    Leitura dos arquivos de entrada    #
        #########################################
        #   conversao da imagem para a matrix que a representa
        print("Lendo a imagem:")
        imageMatrix = readImage(imageInput)
        
        #   eliminamos as quebras de linha do arquivo texto
        print("Eliminando espaco e caracteres especiais do texto a ser codificado:")
        changeNewLine(txtInput, txtInput)

        #   conversao do texto (escrito) para binario
        binText = txtToBin(txtInput)

        ####################################
        #    Codifica o texto na imagem    #
        ####################################
        print("Codificando o texto na imagem:")
        encodedImgMatrix = encodeImage(imageMatrix, binText, bitPlane)

        ###############################
        #    Armazena a nova image    #
        ###############################
        print("Armazenando imagem modificada:")
        storeImage(imageOutput, encodedImgMatrix)

        # debug
        # writePlans(encodedImgMatrix)

    elif operation == "decodificar":
        print("Decodificando")
    else: 
        print("Operation not supported!")

if __name__ == '__main__':
    main()
