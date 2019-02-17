import requests

def download_patch(lat_long,api_key,zoom=19,dimensions=(1000,1000),file_format='png'):
    latitude, longitude = lat_long
    x, y = dimensions
    URL = ('https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/{},{}/'
            '{}?mapSize={},{}&format={}&key={}').format(latitude,longitude,zoom,x,y,file_format,api_key)
    response = requests.get(URL)
    return response