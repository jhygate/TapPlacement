from flask import Flask, request, Response, jsonify
import requests
import cv2
import base64
import numpy
import TapWork, recolour, resize, contours, map_downloader

API_KEY = 'PLACEHOLDER'

app = Flask(__name__)

def toBase64(image):
    _, buffer = cv2.imencode('.png', image)
    png_as_text = base64.b64encode(buffer).decode('utf-8')
    return png_as_text

def process(coords, image):
    max_size = 200
    resized_image = resize.resize(image,max_size)
    height, width, _ = resized_image.shape
    recoloured_image = recolour.find_silver(resized_image)
    houses = contours.get_contour_nodes(recoloured_image)
    tap_locations = TapWork.greedy_brute(houses,5,(height,width))
    image = TapWork.draw_network(houses,tap_locations,resized_image,display=False) 
    return toBase64(image)

@app.route('/giveLocation', methods=['GET'])
def giveLocation():
    lon = request.args.get('long')
    lat = request.args.get('lat')
    print(lon,lat)
    if lon is None or lat is None:
        response = Response()
        response.status_code = 400
        return response
    response = map_downloader.download_patch((lon,lat),API_KEY)
    image_array = numpy.asarray(bytearray(response.content), dtype=numpy.uint8)
    map_image = cv2.imdecode(image_array, -1)
    base64_payload = process((lon,lat),map_image)
    return jsonify(image=base64_payload)

if __name__ == '__main__':
    app.run()