# 2018/12/30 22:21
# 2018/12/30 23:25

import cv2

img = cv2.imread("resized.jpg")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)

rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

mask = cv2.inRange(rgb, (150,160,160), (255, 255, 255))
dst1 = cv2.bitwise_and(img, img, mask=mask)

th, threshed = cv2.threshold(v, 150, 255, cv2.THRESH_BINARY_INV)
dst2 = cv2.bitwise_and(img, img, mask=threshed)

th, threshed2 = cv2.threshold(s, 30, 255, cv2.THRESH_BINARY_INV)
dst3 = cv2.bitwise_and(img, img, mask=threshed2)

cv2.imwrite("dst1.png", dst1)
cv2.imwrite("dst2.png", dst2)
cv2.imwrite("dst3.png", dst3)

from PIL import Image

# Separate RGB arrays
im = Image.open('dst1.png', 'r')
R, G, B = im.convert('RGB').split()
r = R.load()
g = G.load()
b = B.load()
w, h = im.size




# for i in range(w):
#     for j in range(h):
#         if(r[i, j] == 0 and g[i, j] == 0 or b[i, j] == 0):
#             r[i, j] = 255
#             # Just change R channel

for i in range(w):
    for j in range(h):
        if(r[i, j] != 0 or g[i, j] != 0 or b[i, j] != 0):
            r[i, j] = 255 # Just change R channel

# Merge just the R channel as all channels
im = Image.merge('RGB', (R, R, R))
im.save("black_and_white.png")