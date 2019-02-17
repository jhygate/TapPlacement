import folium

#token = "pk...." # your mapbox token
#tileurl = 'https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(token)

m = folium.Map(
    location=[48.73596, 11.18434], zoom_start=9)#, tiles=tileurl, attr='Mapbox')

m = m.build_map()
