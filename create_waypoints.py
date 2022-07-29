import numpy as np
import os
import glob
from shapely.geometry import Polygon, Point

if __name__ == "__main__":
    # get list of files that matches pattern
    files = list(filter(os.path.isfile, glob.glob("*.poly")))
    
    # sort by modified time
    files.sort(key=lambda x: os.path.getmtime(x))
    
    # get last item in list
    lastfile = files[-1]
    
    print("Using data from: {}".format(lastfile))
    
    poligon = open(lastfile)
    poligon = poligon.readlines()
    poli = []
    
    for l in poligon[1:]:
        poli.append(l.strip().split(" "))
    
    poligon = np.zeros([len(poli),len(poli[0])])
    
    for i in range(len(poli)):
        for j in range(len(poli[0])):
            poligon [i,j] = (float(poli[i][j]))
             
    lat = poligon.transpose()[0]
    lon = poligon.transpose()[1]
    #plt.plot(lon,lat,"o-")
    polygon = Polygon(poligon)
    latmin, lonmin, latmax, lonmax = polygon.bounds
    resolution = 20/111390
    
    waypoints = [0]
    for i in np.arange(latmin-resolution/2, latmax, resolution):
        for j in np.arange(lonmin-resolution/2, lonmax, abs(resolution/np.cos(latmin*np.pi/180))):
            if latmax-latmin < resolution:
                i = (latmax+latmin)/2
            if lonmax-lonmin < abs(resolution/np.cos(latmin*np.pi/180)):
                j = (lonmax+lonmin)/2
            if polygon.contains(Point(i,j)):
                waypoints.append(i)
                waypoints.append(j)
    
    waypoints.append(0)
    waypoints_list = [waypoints]

    outfile = open('waypoints.txt', 'w')
    
    for number in waypoints_list:
        outfile.write(str(number))
        
    outfile.close()
    #plt.plot(lon-lonmin,lat-latmin,"o-")            
    #plt.plot(points_lon,points_lat, "o")