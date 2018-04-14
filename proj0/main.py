from manageImage import ManageImage
import os

def main():

    path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/images/'
    #filename = str(input("Enter the image name: "))

    for filename in os.listdir(path):
        # invoke the object
        manager = ManageImage(path,filename)
        # here we call the method that reads the png image
        image = manager.readImage()
        # here we plot the histogram of the given image
        manager.imageHistogram(image)
        # here we plot the statics of the given image
        manager.imageStatics(image)
        # here we plot the negative of an image
        manager.imageNegative(image)
        # here we change the range color of the image
        manager.convertImageRange(image,120)

if __name__ == '__main__':
    main()
