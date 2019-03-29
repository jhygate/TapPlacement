import cv2
import numpy

def find_silver(image):
    image = cv2.GaussianBlur(image,(5,5),0)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    cv2.imshow("HSV", hsv)
    cv2.waitKey();

    mask2 = cv2.inRange(hsv, (10,0,120), (85, 70, 255))
    # mask2 = cv2.inRange(hsv, (0,0,180), (255, 255, 255))


    cv2.imshow("mask2", mask2)

    newimage = cv2.bitwise_and(rgb, rgb, mask=mask2)
    mask = cv2.inRange(rgb, (150,150,140), (255, 255, 255))



    cv2.imshow("mask", mask)
    cv2.waitKey();


    return mask