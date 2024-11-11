#!/usr/bin/env python3
from staticmap import StaticMap, CircleMarker

# Coordinates for Sarinah Mall, Jakarta
latitude, longitude = -6.1890, 106.8231

# Use Stamen Toner Lite tiles for a minimalist, road-focused map
map = StaticMap(600, 400, url_template="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

# Add a transparent marker at Sarinah Mall
transparent_marker = CircleMarker((longitude, latitude), '#FFFFFF', 0)  # Fully transparent
map.add_marker(transparent_marker)

# Render and save the map to an image file
image = map.render(zoom=14)  # Adjust zoom level as needed
image.save('sarinah.png')

