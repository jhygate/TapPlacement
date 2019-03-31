import cv2
import numpy

def find_silver(image):
    # Blur image to reduce noise
    image = cv2.GaussianBlur(image,(5,5),0)
    # Get hsv and rgb channels
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    # use HSV to remove dark areas
    firstmask = cv2.inRange(hsv, (10,0,120), (85, 70, 255))

    #  Use RGB to mask buildings
    newrgb = cv2.bitwise_and(rgb, rgb, mask=firstmask)

    mask = cv2.inRange(newrgb, (150,150,140), (255, 255, 255))
    return mask

