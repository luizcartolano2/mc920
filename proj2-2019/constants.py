__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "terminated"
__version__ = "1.0"
__date__    = "14 march 2019"


import os


#   paths para a pasta
PROJ_PATH = os.getcwd()
WKS_PATH = os.path.abspath(os.path.join(PROJ_PATH, os.pardir))
IMAGE_PATH = PROJ_PATH + '/inputs/'
OUTPUT_PATH = PROJ_PATH + '/outputs/'
