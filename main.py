import resize
import recolour
import contours
import TapWork
import map_downloader
import cv2
import numpy as np

response = map_downloader.download_patch((13.623299, -15.192386),)
image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
map_image = cv2.imdecode(image_array, -1)
max_size = 200
resized_image = resize.resize(map_image,max_size)
height, width, _ = resized_image.shape
recoloured_image = recolour.find_silver(resized_image)
houses = contours.get_contour_nodes(recoloured_image)
TapWork.greedy_brute(houses,5,(height,width),resized_image)
