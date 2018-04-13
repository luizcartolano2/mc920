import cv2
from matplotlib import pyplot as plt

def calcHist(filename):
    # read the image png
    img = cv2.imread(filename,0)
    # calc and plot the image histogram
    plt.hist(img.ravel(),256,[0,256]); plt.show()

def main():
    # setting the path to image
    path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/images/'
    filename = str(input("Enter the image name: "))
    filename = path + filename

    calcHist(filename)

if __name__ == '__main__':
    main()
