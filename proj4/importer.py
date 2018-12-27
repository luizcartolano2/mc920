import pip
from pip._internal import main


def install(package):
    """

    Function to download the dependences used by the code

    :param package: name of the package that should be installed
    :return: None

    """
    if hasattr(pip, 'main'):
        try:
            pip.main(['install', package])
            return True
        except Exception as e:
            print("Nao foi possivel baixar o pacote " + package + " pois " + str(e))
            return False
    else:
        try:
            main(['install', package])
            return True
        except Exception as e:
            print("Nao foi possivel baixar o pacote " + package + " pois " + str(e))
            return False
