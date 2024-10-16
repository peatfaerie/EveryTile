#!/usr/bin/env python3

import math
import sys

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 1 << zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: deg2int.py <lat> <lon> [zoom]")
        return
    
    try:
        lat = float(sys.argv[1])
        lon = float(sys.argv[2])
        zoom = int(sys.argv[3]) if len(sys.argv) == 4 else 14
        xtile, ytile = deg2num(lat, lon, zoom)
        print(f"{xtile} {ytile}")
    
    except ValueError:
        print("Please provide valid numerical values for lat, lon, and optionally zoom.")

if __name__ == "__main__":
    main()
