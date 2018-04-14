import cv2
from numpy import rint
import matplotlib.pyplot as plt
import os

class ManageImage(object):
    """docstring for [object Object]."""
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

    """ Method to read an image """
    def readImage(self):
        # path to the file
        filename = self.path + self.filename
        # read the image
        image_matrix = cv2.imread(filename,0)
        # return the image readed
        return image_matrix

    """ Method to plot the histogram of an image """
    def imageHistogram(self, image_matrix):
        plt.hist(image_matrix.ravel(), bins=256, range=[0, 256])
        plt.title('Intensity Histogram')
        plt.xlabel('Levels of intensity')
        plt.ylabel('Frequency')
        # determine the path where we are going to save our histogram
        path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj0/histograms'
        filepath = os.path.join(path, self.filename)
        plt.savefig(filepath)

    """ Method to show the dimensions of an image """
    def imageDimensions(self, image_matrix):
        height, width = image_matrix.shape[:2]

        return height,width

    """ Method to show the dimensions of an image """
    def intensityValues(self, image_matrix):
        # find image min and max intensity
        min, max, a, b = cv2.minMaxLoc(image_matrix)
        # find the mean image intensity
        mean = cv2.mean(image_matrix)

        return int(min), int(max), mean[0]

    """ Method to show the statics of an image """
    def imageStatics(self, image_matrix):
        # replace the .png to .txt at the filename
        filename = self.filename.replace(".png",".txt")
        # find image height and size
        height, width = self.imageDimensions(image_matrix)
        # find image min, max and mean intensity
        min, max, mean = self.intensityValues(image_matrix)
        # open the file where we are going to write
        path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj0/statics'
        filepath = os.path.join(path, filename)
        f = open(filepath,"w+")
        # print infos in a file
        f.write('Width: ' + str(height) + '\n')
        f.write('Height: ' + str(width) + '\n')
        f.write('Minimum level of intensity: ' + str(min) + '\n')
        f.write('Maximum level of intensity: ' + str(max) + '\n')
        f.write('Average level of intensity: ' + str(mean) + '\n'   )
        f.write('\n')
        f.close

    """ Method to find the negative of an image """
    def imageNegative(self, image_matrix):
        # invert the image
        img = cv2.bitwise_not(image_matrix)

        # store the image negative
        path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/modifiedImages/negative/'
        self.storeImage(path, img)

    """ Method to change the range colors of an image """
    def convertImageRange(self, image_matrix, lowRange):
        img = rint(image_matrix * ((lowRange/2)/255.0)) + lowRange

        # store the image negative
        path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/modifiedImages/range/'
        self.storeImage(path, img)

    """ Method to store new modified images """
    def storeImage(self, path, image_matrix):
        filename = path + self.filename
        cv2.imwrite(filename, image_matrix)
