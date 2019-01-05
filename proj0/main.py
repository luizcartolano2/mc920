__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "terminated"
__version__ = "1.1"
__date__    = ""

try:
    from manageImage import ManageImage
    import os
except ImportError:
    raise SystemExit

path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/images/'


def main():

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
