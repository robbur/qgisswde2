#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from swde_to_postgis_class import SwdeToPostgis

def main():
    
    swde_file = str(sys.argv[1])
    tablistString = sys.argv[2]
    srid = sys.argv[3]
    pyproj4strFrom = sys.argv[4]
    pyproj4strTo = sys.argv[5]
    rodz_importu = sys.argv[6]
    pgserver = sys.argv[7]
    pgbase = sys.argv[8]
    pguser = sys.argv[9]
    pguserpswd = sys.argv[10]
    txtcodec = sys.argv[11]
    id_zd = sys.argv[12]
    
    swdeimport = SwdeToPostgis(swde_file, tablistString, srid, pyproj4strFrom, pyproj4strTo, rodz_importu, pgserver, pgbase, pguser, pguserpswd, txtcodec, id_zd)
    swdeimport.importuj_plik()
    #ponizsze tylkpo po to, zeby zatrzymac zewnetrzna konsole otwarta
    a = raw_input("wcisnij se entera")
    
    
    
#------------------------------------------------------------------------------------------------------#        

main()

