__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "terminated"
__version__ = "1.3"
__date__    = "12 december 2018"

try:
    from importer import install
    from constants import PATH_IN, PATH_OUT_HOR, PATH_OUT_HOUGH
    import logging
    import os
    import threading
except ImportError:
    raise SystemExit

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

try:
    from basicImage import read_image, store_image, rotate_image
    from imageAlign import hough_transform, horizontal_projection
except ImportError:
    raise SystemExit


def align_image(filename):
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
    image_matrix = read_image(PATH_IN + filename)
    if image_matrix.size == 0:
        logger.warning(filename + ' nao foi lido corretamente!')
        return
    else:
        logger.info(filename + ' lido corretamente!')

    ##################################
    #   APLICA TECNICAS DE ROTACAO   #
    ##################################
    #   tecnica da projecao horizontal
    print("\tAplicando a tecnica da projecao Horizontal:")
    proj_angle = horizontal_projection(image_matrix)
    if proj_angle is None:
        logger.warning(filename + " falha ao aplicar a tecnica da projecao horizontal.")
        return
    logger.info("Angulo calculado pela projecao Horizontal: " + str(proj_angle) + " para o arquivo: " + filename)

    #   tecnica da transformada de Hough
    print("\tAplicando a tecnica da transformada de Hough:")
    #   pega o angulo a ser transformado
    hough_angle = hough_transform(image_matrix)
    if hough_angle is None:
        logger.warning(filename + " falha ao aplicar a tecnica da transformada de hough.")
        return
    logger.info("Angulo calculado pela transformada de Hough: " + str(hough_angle) + " para o arquivo: " + filename)

    ############################
    #   ROTACIONA AS IMAGENS   #
    ############################
    #   salva a imagem pos projecao Horizontal
    print("\tSalvando imagem apos aplicacao da projecao Horizontal: ")
    proj_image = rotate_image(image_matrix, proj_angle)
    if proj_image.size == 0:
        logger.warning(filename + ' nao foi rotacionado corretamente pela projecao horizontal.')
        return
    else:
        logger.info(filename + ' rotacionado corretamente pela projecao horizontal.')

    #   salva a imagem pos transformada de Hough
    print("\tSalvando imagem apos aplicacao da transformada de Hough: ")
    hough_image = rotate_image(image_matrix, hough_angle)
    if hough_image.size == 0:
        logger.warning(filename + ' nao foi rotacionado corretamente pela transformacao de Hough.')
        return
    else:
        logger.info(filename + ' rotacionado corretamente pela transformacao de Hough.')

    #####################################
    #   SALVA AS IMAGENS ROTACIONADAS   #
    #####################################
    #   salva a imagem rotacionada pela projecao horizontal
    if not store_image(PATH_OUT_HOR + filename, proj_image):
        logger.warning(filename + " nao foi salvo corretamente apos aplicacao da projecao horizontal.")
    else:
        logger.info(filename + " salvo corretamente apos aplicacao da projecao horizontal.")

    #   salva a imagem rotacionada pela transformada de Hough
    if not store_image(PATH_OUT_HOUGH + filename, hough_image):
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

    for filename in os.listdir(PATH_IN):
        files.append(filename)

    for i in range(len(files)):
        t = threading.Thread(target=align_image, args=(files[i],))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
