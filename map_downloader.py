import requests

def download_patch(lat_long,api_key,zoom=19,dimensions=(1000,1000),file_format='png'):
    latitude, longitude = lat_long
    x, y = dimensions
    URL = ('https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/{},{}/'
            '{}?mapSize={},{}&format={}').format(latitude,longitude,zoom,x,y,file_format)
    print("Downloading the map from {}".format(URL))
    image = requests.get(("{}&key={}").format(URL, api_key))
    # metadata = requests.get(("{}&mapMetadata=1&key={}").format(URL, api_key))
#     boundingbox = metadata.json()["resourceSets"][0]["resources"][0]["bbox"]
    # print(metadata.text);
    return image