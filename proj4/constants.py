__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "terminated"
__version__ = "1.0"
__date__    = ""

import os

#   paths para a pasta
PROJ_PATH = os.getcwd()
WKS_PATH = os.path.abspath(os.path.join(PROJ_PATH, os.pardir))
IMAGE_PATH = WKS_PATH + '/images/'
OUTPUT_PATH = PROJ_PATH + '/output/'
