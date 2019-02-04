import cv2
import numpy as np
import pyautogui
import random
import time
from imutils.object_detection import non_max_suppression
from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = "/usr/local/Cellar/tesseract/4.0.0/bin/tesseract"

def region_grabber(region):
    """
    grabs a region (topx, topy, bottomx, bottomy)
    to the tuple (topx, topy, width, height)
    input : a tuple containing the 4 coordinates of the region to capture
    output : a PIL image of the area selected.
    """
    x1 = region[0]
    y1 = region[1]
    width = region[2]-x1
    height = region[3]-y1

    return pyautogui.screenshot(region=(x1,y1,width,height))


def image_search_area(image, x1, y1, x2, y2, precision=0.8, im=None):
    """
    Searchs for an image within an area
    input :
    image : path to the image file (see opencv imread for supported types)
    x1 : top left x value
    y1 : top left y value
    x2 : bottom right x value
    y2 : bottom right y value
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
    im : a PIL image, usefull if you intend to search the same unchanging region for several elements
    returns :
    the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not
    """
    if im is None :
        im = region_grabber(region=(x1, y1, x2, y2))
        #im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def click_image(image, pos, action, timestamp, offset=5):
    """
    click on the center of an image with a bit of random.
    eg, if an image is 100*100 with an offset of 5 it may click at 52,50 the first time and then 55,53 etc
    Usefull to avoid anti-bot monitoring while staying precise.
    this function doesn't search for the image, it's only ment for easy clicking on the images.
    input :
    image : path to the image file (see opencv imread for supported types)
    pos : array containing the position of the top left corner of the image [x,y]
    action : button of the mouse to activate : "left" "right" "middle", see pyautogui.click documentation for more info
    time : time taken for the mouse to move from where it was to the new position
    """
    img = cv2.imread(image)
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0] + r(width / 2, offset), pos[1] + r(height / 2,offset),
                     timestamp)
    pyautogui.click(button=action)


def image_search(image, precision=0.8):
    """
    Searchs for an image on the screen
    input :
    image : path to the image file (see opencv imread for supported types)
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
    im : a PIL image, usefull if you intend to search the same unchanging region for several elements
    returns :
    the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not
    """
    im = pyautogui.screenshot()
    #im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1,-1]
    return max_loc


def imagesearch_loop(image, timesample, precision=0.8):
    """
    Searchs for an image on screen continuously until it's found.
    input :
    image : path to the image file (see opencv imread for supported types)
    time : Waiting time after failing to find the image
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
    returns :
    the top left corner coordinates of the element if found as an array [x,y]
    """
    pos = image_search(image, precision)
    while pos[0] == -1:
        print(image+" not found, waiting")
        time.sleep(timesample)
        pos = image_search(image, precision)
    return pos


def imagesearch_numLoop(image, timesample, maxSamples, precision=0.8):
    """
    Searchs for an image on screen continuously until it's found or max number of samples reached.
    input :
    image : path to the image file (see opencv imread for supported types)
    time : Waiting time after failing to find the image
    maxSamples: maximum number of samples before function times out.
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
    returns :
    the top left corner coordinates of the element if found as an array [x,y]
    """
    pos = image_search(image, precision)
    count = 0
    while pos[0] == -1:
        print(image+" not found, waiting")
        time.sleep(timesample)
        pos = image_search(image, precision)
        count = count + 1
        if count>maxSamples:
            break
    return pos


def imagesearch_region_loop(image, timesample, x1, y1, x2, y2, precision=0.8):
    """
    Searchs for an image on a region of the screen continuously until it's found.
    input :
    image : path to the image file (see opencv imread for supported types)
    time : Waiting time after failing to find the image
    x1 : top left x value
    y1 : top left y value
    x2 : bottom right x value
    y2 : bottom right y value
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
    returns :
    the top left corner coordinates of the element as an array [x,y]
    """
    pos = image_search_area(image, x1,y1,x2,y2, precision)

    while pos[0] == -1:
        time.sleep(timesample)
        pos = image_search_area(image, x1, y1, x2, y2, precision)
    return pos


def imagesearch_count(image, precision=0.9):
    """
    Searches for an image on the screen and counts the number of occurrences.
    input :
    image : path to the target image file (see opencv imread for supported types)
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.9
    returns :
    the number of times a given image appears on the screen.
    optionally an output image with all the occurances boxed with a red outline.
    """
    img_rgb = pyautogui.screenshot()
    img_rgb = np.array(img_rgb)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= precision)
    count = 0
    for pt in zip(*loc[::-1]):  # Swap columns and rows
        #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2) // Uncomment to draw boxes around found occurances
        count = count + 1
    #cv2.imwrite('result.png', img_rgb) // Uncomment to write output image with boxes drawn around occurances
    return count


def r(num, rand):
    return num + rand*random.random()


def save_textarea(image, east="/Users/luizeduardocartolano/Dropbox/DUDU/python-test/automate_test/frozen_east_text_detection.pb",
                   min_confidence=0.35, width=640, height=640):
    # load the input image and grab the image dimensions
    image = cv2.imread(image)
    orig = image.copy()
    (origH, origW) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    rW = origW / float(newW)
    rH = origH / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east)

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
        (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(scores, geometry, min_confidence)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        temp = orig[startY:startY+(endY-startY), startX:startX+(endX-startX)]
        cv2.imshow("Text Detection", temp)
        # cv2.imshow("Text Detection", orig)
        cv2.waitKey(0)


def text_detection(image, east="/Users/luizeduardocartolano/Dropbox/DUDU/python-test/automate_test/frozen_east_text_detection.pb",
                   min_confidence=0.35, width=640, height=640):
    # load the input image and grab the image dimensions
    image = cv2.imread(image)
    orig = image.copy()
    (origH, origW) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    rW = origW / float(newW)
    rH = origH / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east)

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
        (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(scores, geometry, min_confidence)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # extract the actual padded ROI
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 0, 255), 2)

        # show image
        cv2.imshow("Text Detection", orig)
        cv2.waitKey(0)


def decode_predictions(scores, geometry, min_confidence):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability,
            # ignore it
            if scoresData[x] < min_confidence:
                continue

            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)


def extract_text(image, east="/Users/luizeduardocartolano/Dropbox/DUDU/python-test/automate_test/frozen_east_text_detection.pb", min_confidence=0.35, width=640, height=640, padding=0):
    # load the input image and grab the image dimensions
    image = cv2.imread(image)
    orig = image.copy()
    (origH, origW) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    rW = origW / float(newW)
    rH = origH / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east)

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
        (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(scores, geometry, min_confidence)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        dX = int((endX - startX) * padding)
        dY = int((endY - startY) * padding)

        # apply padding to each side of the bounding box, respectively
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(origW, endX + (dX * 2))
        endY = min(origH, endY + (dY * 2))

        # extract the actual padded ROI
        roi = orig[startY:endY, startX:endX]

        # in order to apply Tesseract v4 to OCR text we must supply
        # (1) a language, (2) an OEM flag of 4, indicating that the we
        # wish to use the LSTM neural net model for OCR, and finally
        # (3) an OEM value, in this case, 7 which implies that we are
        # treating the ROI as a single line of text
        config = ("-l eng --oem 1 --psm 7")
        text = pytesseract.image_to_string(roi, config=config)

        # add the bounding box coordinates and OCR'd text to the list
        # of results
        results.append(((startX, startY, endX, endY), text))

    # sort the results bounding box coordinates from top to bottom
    results = sorted(results, key=lambda r:r[0][1])

    # loop over the results
    for ((startX, startY, endX, endY), text) in results:
        # display the text OCR'd by Tesseract
        print("OCR TEXT")
        print("========")
        print("{}\n".format(text))

        # strip out non-ASCII text so we can draw the text on the image
        # using OpenCV, then draw the text and a bounding box surrounding
        # the text region of the input image
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        output = orig.copy()
        cv2.rectangle(output, (startX, startY), (endX, endY),
            (0, 0, 255), 2)
        cv2.putText(output, text, (startX, startY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        # show the output image
        cv2.imshow("Text Detection", output)
        cv2.waitKey(0)
