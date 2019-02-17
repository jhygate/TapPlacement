# import the necessary packages
import imutils
import cv2

# construct the argument parse and parse the arguments
def get_contour_nodes(image):
    height, width, channels = image.shape
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    nodes = []

    # loop over the contours
    for c in cnts:
        # compute the center of the contour
        try:
            if cv2.contourArea(c) > 40:
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                nodes.append([cv2.contourArea(c), [cX, cY]])
        except:
            pass
    return nodes