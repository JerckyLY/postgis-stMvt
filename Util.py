import math

def tile2lat(ytile,zoom):
    n = 2.0 ** zoom
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg

def tile2lon(xtile,zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    return lon_deg

# [lonmin  lonmax]
def getLon(xtile,zoom):
    a = []
    a.append(tile2lon(xtile,zoom))
    a.append(tile2lon(xtile+1,zoom))
    return a
#[latmin,latmax]
def getLat(ytile,zoom):
    a = []
    a.append(tile2lat(ytile,zoom))
    a.append(tile2lat(ytile+1,zoom))
    return a


# print("lonmin: %f"%getLon(840,10)[0])
# print("lonmax: %f"%getLon(840,10)[1])
#
# print("latmin: %f"%getLat(622,10)[0])
# print("latmax: %f"%getLat(622,10)[1])

