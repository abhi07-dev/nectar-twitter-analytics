# Instructions to install Shapely (using wheels) python library and how to use it
# Library URL: https://pypi.org/project/Shapely/
# 1. Go to url http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely
# 2. Download shapely wheel file (as per Python installed version) ex: Shapely‑1.6.4.post1‑cp35‑cp35m‑win_amd64.whl >> for python v3.5 and 64 bit
# 3. Run command: pip install Shapely‑1.6.4.post1‑cp35‑cp35m‑win_amd64.whl
# 4. Program requires Shapefile and it's link to be defined in line 11 (it requires all 4 types of shapefile VIC_LOCALITY_POLYGON_shp.dbf, VIC_LOCALITY_POLYGON_shp.shp)

import shapefile
from shapely.geometry import Polygon, shape, Point

r = shapefile.Reader("VIC_LOCALITY_POLYGON_shp.dbf")

# get the shapes
shapes = r.shapes()
records = r.records()

# print (len(shapes))
# print (len(records))

def check(polygon, lon, lat):
    # build a shapely point from your geopoint
    point = Point(lon, lat)

    # the contains function does exactly what you want
    return polygon.contains(point)


def locateSuburb (lon, lat):

    shapeNbr = ""
    subName = 'Not Available'
    
    for x in range(len(shapes)):
        polygon = shape(shapes[x]) 
        status = check(polygon, lon, lat)
        if (status == True):
            # print ("Point Found")
            # print (polygon)
            # bbox = shapes[x].bbox
            # print (bbox)
            shapeNbr = x
            break

    for i in range(len(records)):
        if (i == shapeNbr):
            subName = records[i][6]
            # print (subName)

    return subName

lon = 144.963730
lat = -37.778165

subName = locateSuburb(lon, lat)
# print (subName)

# build a shapely polygon from your shape
# polygon = shape(shapes[0])    

# status = check(141.74552471, -35.12767701)
# print (status)



