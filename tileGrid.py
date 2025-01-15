#!/usr/bin/env python3
import argparse
import math

parser = argparse.ArgumentParser(description="create tilehunting grid")
parser.add_argument("LAT", help="latitude of area center", type=float)
parser.add_argument("LON", help="longitude of area center", type=float)
parser.add_argument("X", help="number of columns", type=int)
parser.add_argument("Y", help="number of lines", type=int)
parser.add_argument("OUTFILE", help="where to write, will be replaced if exist")

args = parser.parse_args()

zoom = 14

#from https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

centertilenum  = deg2num(args.LAT, args.LON, zoom)

#TODO: test and modify to work on both sides of prime median and equator (even around)
#TODO: currenty tested just for central Europe

xMinTileNum = centertilenum[0] - math.ceil((args.X-1)/2)
yMinTileNum = centertilenum[1] - math.ceil((args.Y-1)/2)
xMaxTileNum = centertilenum[0] + math.floor((args.X-1)/2)
yMaxTileNum = centertilenum[1] + math.floor((args.Y-1)/2)

latMax, lonMin = num2deg(xMinTileNum, yMinTileNum, zoom)
latMin, lonMax = num2deg(xMaxTileNum+1, yMaxTileNum+1, zoom)

with open(args.OUTFILE, "w") as f:

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://earth.google.com/kml/2.1"> <Document>\n')
    f.write('<Style id="normal">\n')
    f.write('  <LineStyle>\n')
    f.write('    <color>ffffffff</color>\n')
    f.write('    <width>1</width>\n')
    f.write('  </LineStyle>\n')
    f.write('  </Style>\n')
    f.write('<Placemark>\n')
    f.write('<styleUrl>#normal</styleUrl>\n')
    f.write('<MultiGeometry>\n')
    #write vertical lines
    x = xMinTileNum
    while x <= xMaxTileNum+1:
        lat, lon = num2deg(x, yMinTileNum, zoom)
        f.write('    <LineString>\n')
        f.write(f'      <coordinates>{lon},{latMax} {lon},{latMin}</coordinates>\n')
        f.write('    </LineString>\n')
        x+=1
    #write horizontal lines
    y = yMinTileNum
    while y <= yMaxTileNum+1:
        lat, lon = num2deg(xMinTileNum, y, zoom)
        f.write('    <LineString>\n')
        f.write(f'      <coordinates>{lonMax},{lat} {lonMin},{lat}</coordinates>\n')
        f.write('    </LineString>\n')
        y+=1
    f.write('</MultiGeometry>\n')
    f.write('</Placemark>\n')
    f.write('</Document> </kml>\n')

