import os
from manageImage import ManageImage

def main():
    path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/objectsImage/'
    # filename = str(input("Enter the image name: "))

    for filename in os.listdir(path):
        # invoke the object
        manager = ManageImage(path,filename)
        # here we read the image
        image = manager.readImage()
        # here we convert the colour image to gray
        gray_img = manager.convertToGray(image)
        # here we contour the objects
        contour_img, binary_img = manager.contourObjetcts(image, gray_img)
        areas = manager.imageProperties(binary_img, gray_img)
        manager.classifyRegions(areas)
        manager.createHistogram(areas)


if __name__ == '__main__':
    main()
