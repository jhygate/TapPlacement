import cv2

def resize(image,max_size):
    img = cv2.imread(image)
    height, width, channels = img.shape
    print(height,width)
    scale = max_size/(max(height,width))
    small = cv2.resize(img, (0,0), fx=scale, fy=scale)
    height,width,channels = small.shape

    cv2.imwrite('resized.jpg',small)

    return height,width