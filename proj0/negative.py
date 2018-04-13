import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def negative(filename):
    path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/images/'
    image = path + filename
    # open the image
    img = cv2.imread(image,0)
    # invert the image
    img = cv2.bitwise_not(img)
    # call the function that create the new modified image
    showImage(filename, img)


def showImage(filename, image):
    # show the inverted image
    newFile = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/modifiedImages/'
    newFile = newFile + filename
    cv2.imwrite(newFile, image)

def main():
    # setting the path to image
    filename = str(input("Enter the image name: "))

    negative(filename)

if __name__ == '__main__':
    main()
