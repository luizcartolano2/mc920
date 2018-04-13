import cv2
from numpy import rint

def negative(filename):
    path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/images/'
    image = path + filename
    # open the image
    img = cv2.imread(image,0)
    img = rint(img * (60.0/255.0)) + 120

    showImage(filename,img)

def showImage(filename, image):
    # show the inverted image
    newFile = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/modifiedImages/range/'
    newFile = newFile + filename
    cv2.imwrite(newFile, image)


def main():
    # setting the path to image
    filename = str(input("Enter the image name: "))
    negative(filename)

if __name__ == '__main__':
    main()
