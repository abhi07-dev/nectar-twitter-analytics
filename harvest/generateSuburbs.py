import sys,getopt,datetime,codecs

from geoSplit import *
from numpy import arange
from FindCoordinate import locateSuburb

suburbsFile = codecs.open("suburbs", "w+", "utf-8")

for lat in arange(lat_min, lat_max, lat_int):
    for lon in arange(long_min, long_max, long_int):
        suburbsFile.write(('%f %f %s\n' % (lat, lon, locateSuburb(lon, lat).lower())))
    suburbsFile.flush()

print('Done generating suburbs.')
