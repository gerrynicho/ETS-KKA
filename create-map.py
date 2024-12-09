#!/usr/bin/env python3
from staticmap import StaticMap, CircleMarker
import cv2

latitude, longitude = -6.1890, 106.8231
latitude = float(input("Enter latitude: "))
longitude = float(input("Enter longitude: "))

map = StaticMap(600, 400, url_template="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

transparent_marker = CircleMarker((longitude, latitude), '#FFFFFF', 0)
map.add_marker(transparent_marker)

zoom_lvl = int(input("Enter zoom level: "))
file_name = str(input("Enter file name: "))

image = map.render(zoom = zoom_lvl) # set for how close the map is
# JALANIN INI DI ROOT DIRECTORY OF REPO

## filter

want_filter = str(input("Do you want to apply filter? (y/n) : "))
if want_filter == 'y':
    image_path = f'maps/{file_name}.png'
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    equalized = cv2.equalizeHist(img)
    _, binary = cv2.threshold(equalized, 200, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f'maps/{file_name}_filtered.png', binary)
    print(f"Filtered map saved in /maps/{file_name}-filtered.png")
else:
    image.save(f'maps/{file_name}.png')
    print(f"Map saved in /maps/{file_name}.png")



