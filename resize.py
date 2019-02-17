import cv2

img = cv2.imread("village.png")
height, width, channels = img.shape
print(height,width)
scale = 300/(max(height,width))
small = cv2.resize(img, (0,0), fx=scale, fy=scale)

cv2.imwrite('resized.jpg',small)