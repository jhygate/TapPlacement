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

def process(image, meters_squared_per_pixel, size ,taps=3, grid=20):
    downscale = int(size / grid)
    height, width, _ = image.shape
    recoloured_image = recolour.find_silver(image)
    houses, percentage, housearea = contours.get_contour_nodes(recoloured_image, meters_squared_per_pixel)
    tap_locations = TapWork.greedy_brute(houses,taps,(height,width), downscale)
    result = TapWork.draw_network(houses,tap_locations, size, image, meters_squared_per_pixel) 
    population = round(housearea / 7)
    recommendation = round(population / 250)
    if recommendation == 0:
        recommendation = 1
    return dict(image=toBase64(result), original=toBase64(image), houses=len(houses), taps=taps, percentage=percentage, area=round(housearea), population=population, recommendation=recommendation)

@app.route('/giveLocation', methods=['GET'])
def giveLocation():
    lon = request.args.get('long')
    lat = request.args.get('lat')
    size = request.args.get('size')
    taps = request.args.get('taps')
    grid = request.args.get('grid')
    zoom = request.args.get('zoom')
    print(lon,lat)
    if lon is None or lat is None:
        response = Response()
        response.status_code = 400
        return response
    if zoom is None:
        zoom = 19
    if size is None:
        size = 1000

    map_image, meters_squared_per_pixel = map_downloader.download_patch((lat,lon), credentials.API_KEY, size, zoom=int(zoom))
    if size is not None and taps is not None and grid is not None:
        result = process(map_image, meters_squared_per_pixel, int(size),taps=int(taps), grid=int(grid))
    elif taps is not None:
        result = process(map_image, meters_squared_per_pixel, int(size), taps=int(taps))
    else:
        result = process(map_image, meters_squared_per_pixel, int(size))

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=25565,host='0.0.0.0')