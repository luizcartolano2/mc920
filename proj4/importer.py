__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "terminated"
__version__ = "1.1"
__date__    = "12 december 2018"

try:
    import pip
    from pip._internal import main as pipmain
    import importlib
except ImportError:
    raise SystemExit


def install_and_import(package):
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        if hasattr(pip, 'main'):
            try:
                pip.main(['install', package, '--no-cache-dir'])
                return True
            except Exception as e:
                print("Nao foi possivel baixar o pacote " + package + " pois " + str(e))
                return False
        else:
            try:
                pipmain(['install', package, '--no-cache-dir'])
                return True
            except Exception as e:
                print("Nao foi possivel baixar o pacote " + package + " pois " + str(e))
                return False

def install(package):
    """

    Function to download the dependences used by the code

    :param package: name of the package that should be installed
    :return: None

    """
    if hasattr(pip, 'main'):
        try:
            pip.main(['install', package, '--no-cache-dir'])
            return True
        except Exception as e:
            print("Nao foi possivel baixar o pacote " + package + " pois " + str(e))
            return False
    else:
        try:
            pipmain(['install', package, '--no-cache-dir'])
            return True
        except Exception as e:
            print("Nao foi possivel baixar o pacote " + package + " pois " + str(e))
            return False
