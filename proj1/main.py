__author__  = "Luiz Cartolano <cartolanoluiz@gmail.com>"
__status__  = "terminated"
__version__ = "1.0"
__date__    = ""

try:
    import os
    from manageImage import ManageImage
    import threading
except ImportError:
    raise SystemExit

path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/objectsImage/'


def main(filename):
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
    files = []
    threads = []

    for filename in os.listdir(path):
        files.append(filename)

    for i in range(len(files)):
        t = threading.Thread(target=main, args=(files[i], ))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

