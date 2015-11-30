#!/usr/bin/python
# -*- coding: utf-8 -*-



from PIL import Image
from PIL.ExifTags import TAGS
import pyproj
from rob_db_connection import RobDBBase
from rob_db_connection import RobDBTable
import sys
import datetime
import os
from dateutil import parser
import Image
import glob

def main():
    
    x_2000 = 5962065.00
    y_2000 = 3585143.01

    p2 = pyproj.Proj("+init=epsg:2177")
    p1 = pyproj.Proj("+init=epsg:2180")

    x_92, y_92 = pyproj.transform(p2,p1,x_2000,y_2000)
    print 'PUWG 92 = ', x_92, y_92

            #values = [filefotopath, str(data), str(czas), point]
            #print values
            #table.insert(0,cols, values)
            #rdbase.commit()
            
            #shell_cmd = "cp " + filepath + " " + filefotopath
            #os.system(shell_cmd)


main()

