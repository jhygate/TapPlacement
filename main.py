import cv2
import numpy as np
import resize
import recolour
import contours
import TapWork
import map_downloader
import credentials

# 13.624999, -15.191250
# 13.623299, -15.192386
response = map_downloader.download_patch((13.623299, -15.192386), credentials.API_KEY)
print("Got map")
image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
map_image = cv2.imdecode(image_array, -1)
max_size = 200
resized_image = resize.resize(map_image, max_size)
height, width, _ = resized_image.shape
# cv2.imwrite("test.png", resized_image)
# cv2.imshow("Window", resized_image)
# cv2.waitKey(0)

recoloured_image = recolour.find_silver(resized_image)
# cv2.imshow("Window", recoloured_image)
# cv2.waitKey(0)

houses, percentage = contours.get_contour_nodes(recoloured_image)
print(houses)
tap_locations = TapWork.greedy_brute(houses, 3, (height, width))
print(tap_locations)
cv2.imwrite("output.png", TapWork.draw_network(houses, tap_locations, resized_image))