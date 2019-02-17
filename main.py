import resize
import messingcolour
import contours
import TapWork
import map_downloader

map_downloader.download_patch((13.323964, -15.9257),'AgqByPum4K6T5wlV3oIAhSDvFHVRuoPs6cwipRdvprWtmvqld0poyLI54AP0e6HI')
max_size = 200
height, width = resize.resize('downloaded.png',max_size)
print(height,width)
messingcolour.find_silver()
houses = contours.get_contour_nodes()
TapWork.greedy_brute(houses,5,(height,width),image='resized.jpg')
