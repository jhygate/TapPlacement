import requests
import math
import numpy
import cv2

def download_patch(lat_long,api_key, size, zoom=19,file_format='png'):
    latitude, longitude = lat_long
    extra = 100
    x, y = size, str((int(size) + extra))
    URL = ('https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/{},{}/'
            '{}?mapSize={},{}&format={}').format(latitude,longitude,zoom,x,y,file_format)
    print("Downloading the map from {}&key={}".format(URL, api_key))
    image = requests.get(("{}&key={}").format(URL, api_key))

    meters_squared_per_pixel = (156543.04 * math.cos(math.radians(float(latitude))) / (2**zoom))**2
    print("Meters squared per pixel: {} ".format(str(meters_squared_per_pixel)))
    # metadata = requests.get(("{}&mapMetadata=1&key={}").format(URL, api_key))
#     boundingbox = metadata.json()["resourceSets"][0]["resources"][0]["bbox"]
    # print(metadata.text);

    image_array = numpy.asarray(bytearray(image.content), dtype=numpy.uint8)
    map_image = cv2.imdecode(image_array, -1)

    # Crop
    map_image = map_image[0:int(size), 0:int(size)]
    return map_image, meters_squared_per_pixel