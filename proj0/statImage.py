import cv2
import numpy as np

def dimensions(filename):
    # open the image
    img = cv2.imread(filename,0)
    # find image height and size
    height, width = img.shape[:2]

    return height,width

def imageIntensity(filename):
    img = cv2.imread(filename,0)

    # find image min and max intensity
    min, max, a, b = cv2.minMaxLoc(img)
    # find the mean image intensity
    mean = cv2.mean(img)

    return int(min), int(max), mean[0]

def main():
    # setting the path to image
    path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/images/'
    filename = str(input("Enter the image name: "))
    filename = path + filename

    height, width = dimensions(filename)
    min, max, mean = imageIntensity(filename)

    print(height)
    print(width)
    print(min)
    print(max)
    print("%.2f" % mean)

if __name__ == '__main__':
    main()
