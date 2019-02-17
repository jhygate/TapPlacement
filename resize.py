import cv2

def resize(image,max_size):
    height, width, channels = image.shape
    scale = max_size/(max(height,width))
    resized_image = cv2.resize(image, (0,0), fx=scale, fy=scale)
    return resized_image