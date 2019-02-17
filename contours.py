# import the necessary packages
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
def get_contour_nodes():
    args = {}
    args["image"] = "black_and_white.png"

    # load the image, convert it to grayscale, blur it slightly,
    # and threshold it
    image = cv2.imread(args["image"])
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
            print(cv2.contourArea(c))
            if cv2.contourArea(c) > 40:
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                nodes.append([cv2.contourArea(c), [cX, cY]])

                # draw the contour and center of the shape on the image
                #cv2.drawContours(image, [c], -1, (0, 0, 255), 2)
                #cv2.circle(image, (cX, cY), 7, (255, 0, 0), -1)
                #cv2.putText(image, "center", (cX - 20, cY - 20),
                 #   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # show the image
                #cv2.imshow("Image", image)


        except:
            pass
    return nodes
