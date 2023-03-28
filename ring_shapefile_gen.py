# create ring shapefile
from shapely.geometry import Point, Polygon, LineString
import geopandas as gpd
import pandas as pd
import math
import matplotlib.pyplot as plt
from bokeh.plotting import show


def sector(center, start_angle, end_angle, radius, steps=200):
    def polar_point(origin_point, angle,  distance):
        return [origin_point.x + math.sin(math.radians(angle)) * distance, origin_point.y + math.cos(math.radians(angle)) * distance]

    if start_angle > end_angle:
        start_angle = start_angle - 360
    else:
        pass
    step_angle_width = (end_angle-start_angle) / steps
    sector_width = (end_angle-start_angle) 
    segment_vertices = []

    segment_vertices.append(polar_point(center, 0,0))
    segment_vertices.append(polar_point(center, start_angle,radius))

    for z in range(1, steps):
        segment_vertices.append((polar_point(center, start_angle + z * step_angle_width,radius)))
    segment_vertices.append(polar_point(center, start_angle+sector_width,radius))
    segment_vertices.append(polar_point(center, 0,0))

    return Polygon(segment_vertices)

center = Point(103.9893, 1.3592)
sect = sector(center, 188, 215, 18.52*1000)
c9 = center.buffer(9/59.9).boundary
c10 = center.buffer(10/59.9).boundary

r9 = c9.difference(c9.difference(sect))
r10 = c10.difference(c10.difference(sect))
print(r9.coords[:])
print(r10.coords[:])
print(type(r10))

rr10 = LineString(r10.reverse().coords[:])
ring_coords = r9.coords[:] + rr10.coords[:]  + [r9.coords[0]]
ring = LineString(ring_coords)
ring

dir_apzone = "Shapefiles/apzone/"

line_string = LineString(ring.coords[:])
coords = line_string.coords[:]
ply_coord = Polygon(coords)
df = {'Attribute': ['name1'], 'geometry': ply_coord}
# Convert shapely object to a geodataframe 
gpd.GeoDataFrame(df, geometry='geometry', crs ="EPSG:4326").to_file(dir_apzone+'approachRing.shp')

# show the shapefile
approachRing = gpd.read_file(dir_apzone + 'approachRing.shp')
fig, ax = plt.subplots()
approachRing.geometry.boundary.plot(ax=ax, color='r', linewidth = 0.5, zorder = 100)
plt.show()


