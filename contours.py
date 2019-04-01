# import the necessary packages
import imutils
import cv2

# construct the argument parse and parse the arguments
def get_contour_nodes(image):
    # Total area is 83,321 m^2
    height, width = image.shape
    totalpixels = height * width

    print(height, width)

    areaperpixel = 83321 / totalpixels

    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image
    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    nodes = []

    totalarea = 0;

    # loop over the contours
    for c in cnts:
        # compute the center of the contour
        try:
            # consider buildings greater than 8m^2
            if cv2.contourArea(c) * areaperpixel > 8:
                M = cv2.moments(c)
                cX = round(M["m10"] / M["m00"])
                cY = round(M["m01"] / M["m00"])
                totalarea += cv2.contourArea(c) * areaperpixel
                nodes.append([cv2.contourArea(c) * areaperpixel, [cX, cY]])
        except:
            pass

    print("average {}".format(totalarea / len(cnts)))
    percentage = round((totalarea / (totalpixels * areaperpixel)) * 100)
    return nodes, percentage, totalarea