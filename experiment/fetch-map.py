#!/usr/bin/env python3
from staticmap import StaticMap, CircleMarker

latitude, longitude = -6.1890, 106.8231

map = StaticMap(600, 400, url_template="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

transparent_marker = CircleMarker((longitude, latitude), '#FFFFFF', 0)  # Fully transparent
map.add_marker(transparent_marker)

image = map.render(zoom=14)
image.save('sarinah.png')

