import cv2
from numpy import shape, empty
import matplotlib.pyplot as plt
import os
import imutils

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
        image_matrix = cv2.imread(filename)
        # return the image readed
        return image_matrix

    """ Method to convert a readed image to gray scale """
    def convertToGray(self, image_matrix):
        # convert image to gray_scale
        gray_img = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)
        # write the path where we are going to save the new image
        path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj1/grayImage/'
        self.storeImage(path,gray_img)

        return gray_img

    """ Method to contour objects of a given image """
    def contourObjetcts(self, image_matrix, gray_img):
        # we find the shapes we want and contour them
        ret, thresh = cv2.threshold(gray_img,190,255,cv2.THRESH_BINARY_INV)
        img, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # create a blank image to draw the contours
        white_image = empty([shape(image_matrix)[0], shape(image_matrix)[1], shape(image_matrix)[2]])
        white_image.fill(255)
        # draw the contours
        image_contours = cv2.drawContours(white_image,contours,-1,(0,255,0),2)
        # path to where we are going to store the contour
        path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj1/contourImages/'
        self.storeImage(path, image_contours)

        return image_contours, thresh

    """ Method to store new modified images """
    def storeImage(self, path, image_matrix):
        filename = path + self.filename
        cv2.imwrite(filename, image_matrix)

    def imageProperties(self, thresh, image):
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        areas = []
        perimeters = []
        i = 0
        for c in cnts:

            areas.append(cv2.contourArea(c))
            perimeters.append(cv2.arcLength(c,True))

            # compute the center of the contour
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # draw the contour and center of the shape on the image
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 2, (255, 255, 255), -1)
            cv2.putText(image, str(i), (cX, cY),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            i = i + 1

        path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj1/centroid/'
        self.storeImage(path,image)

        size = len(areas)
        # replace the .png to .txt at the filename
        filename = self.filename.replace(".png",".txt")
        # open the file where we are going to write
        path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/IC/MC920/workspace/proj1/properties/'
        filepath = os.path.join(path, filename)
        f = open(filepath,"w+")

        f.write("Number of regions: " + str(size) + '\n')
        for i in range(size):
            f.write("Region: " + str(i) + ' ')
            f.write("Perimeter: " + str(areas[i]) + ' ')
            f.write("Área: " + str(perimeters[i]) + ' ')
            f.write('\n')

        f.close()
