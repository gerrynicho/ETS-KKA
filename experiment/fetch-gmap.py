#!/usr/bin/env python3
from staticmap import StaticMap, CircleMarker

latitude, longitude = -6.1890, 106.8231 # sarinah mall

# Use a different OSM tile server for better map loading
map = StaticMap(600, 400, url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png")

# Add a marker at Sudirman Station
marker = CircleMarker((longitude, latitude), 'red', 12)
map.add_marker(marker)

# Render and save the map to an image file
image = map.render(zoom=16)  # Increased zoom level for better detail
image.save('sarinah.png')

