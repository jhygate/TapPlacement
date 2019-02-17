import cv2
import numpy

def find_silver(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)

    rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    mask = cv2.inRange(rgb, (150,160,160), (255, 255, 255))
    image = cv2.bitwise_and(image, image, mask=mask)

    for w in range(image.shape[0]):
        for h in range(image.shape[1]):
            # checks if not pure black
            if(all(rgb != 0 for rgb in image[w][h])):
                # makes pixel completely white
                for colour in range(image.shape[2]):
                    image[w][h][colour] = 255
    return image