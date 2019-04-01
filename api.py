from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
import cv2
import base64
import math
import numpy
import TapWork, recolour, resize, contours, map_downloader, credentials

app = Flask(__name__)
cors = CORS(app)

def toBase64(image):
    _, buffer = cv2.imencode('.png', image)
    png_as_text = base64.b64encode(buffer).decode('utf-8')
    return png_as_text

def process(image, max_size=200,taps=3, downscale=10):
    resized_image = resize.resize(image,max_size)
    height, width, _ = resized_image.shape
    recoloured_image = recolour.find_silver(resized_image)
    houses, percentage, housearea = contours.get_contour_nodes(recoloured_image)
    print(downscale)
    tap_locations = TapWork.greedy_brute(houses,taps,(height,width), downscale)
    image = TapWork.draw_network(houses,tap_locations,resized_image, (height,width)) 
    population = round(housearea / 7)
    recommendation = round(population / 250)
    if recommendation == 0:
        recommendation = 1
    return dict(image=toBase64(image), houses=len(houses), taps=taps, percentage=percentage, area=round(housearea), population=population, recommendation=recommendation)

@app.route('/giveLocation', methods=['GET'])
def giveLocation():
    lon = request.args.get('long')
    lat = request.args.get('lat')
    max_size = request.args.get('size')
    taps = request.args.get('taps')
    downscale = request.args.get('downscale')
    zoom = request.args.get('zoom')
    print(lon,lat)
    if lon is None or lat is None:
        response = Response()
        response.status_code = 400
        return response
    if zoom is None:
        zoom = 19
    image = map_downloader.download_patch((lat,lon), credentials.API_KEY, zoom=int(zoom))
    image_array = numpy.asarray(bytearray(image.content), dtype=numpy.uint8)
    map_image = cv2.imdecode(image_array, -1)
    if max_size is not None and taps is not None and downscale is not None:
        result = process(map_image, max_size=int(max_size),taps=int(taps), downscale=int(downscale))
    elif max_size is not None and taps is not None:
        result = process(map_image, max_size=int(max_size),taps=int(taps))
    elif max_size is not None: 
        result = process(map_image, max_size=int(max_size))
    elif taps is not None:
        result = process(map_image, taps=taps)
    else:
        result = process(map_image)

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=25565,host='0.0.0.0')