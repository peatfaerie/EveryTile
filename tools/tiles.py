#!/usr/bin/env python3

import sys
import numpy as np
import math

def deg2int(x, y, zoom):
    lat_rad = y * math.pi / 180.0
    n = 2.0 ** zoom
    xi = math.floor((x + 180.0) / 360.0 * n)
    yi = math.floor((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return xi, yi

def main():
    if len(sys.argv) < 4:
        print("Usage: tiles.py <file> <hlon> <hlat> [zoom]")
        print("\n[ex.:\ntiles.py tiles14.txt 13.122137 52.428952 14\ntiles.py tiles17.txt 13.122137 52.428952 17]")
        sys.exit(1)

    filename = sys.argv[1]
    hlon = float(sys.argv[2])
    hlat = float(sys.argv[3])
    zoom = int(sys.argv[4]) if len(sys.argv) > 4 else 14

    hx, hy = deg2int(hlon, hlat, zoom)

    d = np.loadtxt(filename)
    A = np.zeros((124, 124), dtype=int)
    x = np.zeros(len(d), dtype=int)
    y = np.zeros(len(d), dtype=int)

    for l in range(len(d)):
        xi, yi = deg2int(d[l, 0] + 0.0001, d[l, 1] - 0.0001, zoom)
        x[l] = xi - hx
        y[l] = yi - hy

    A[np.min(x) + 61 : np.max(x) + 61, np.min(y) + 61 : np.max(y) + 61] = 1
    for l in range(len(x)):
        A[x[l] + 61, y[l] + 61] = 0

    # Create compressed array
    v = np.zeros(124 * 4, dtype=np.int32)
    l = 0
    for ly in range(124):
        for lx in range(4):
            b = A[lx * 31 : (lx + 1) * 31, ly] > 0
            for i in range(31):
                if b[i]:
                    v[l] = v[l] | (1 << i)
            l += 1

    # Create a string for the settings
    str = []
    for l in range(124):
        str.append(chr((v[4 * l + 0] & 0x3f) + 48))
        str.append(chr(((v[4 * l + 0] >> 6) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 0] >> 12) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 0] >> 18) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 0] >> 24) & 0x3f) + 48))

        str.append(chr((v[4 * l + 1] & 0x3f) + 48))
        str.append(chr(((v[4 * l + 1] >> 6) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 1] >> 12) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 1] >> 18) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 1] >> 24) & 0x3f) + 48))

        str.append(chr((v[4 * l + 2] & 0x3f) + 48))
        str.append(chr(((v[4 * l + 2] >> 6) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 2] >> 12) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 2] >> 18) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 2] >> 24) & 0x3f) + 48))

        str.append(chr((v[4 * l + 3] & 0x3f) + 48))
        str.append(chr(((v[4 * l + 3] >> 6) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 3] >> 12) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 3] >> 18) & 0x3f) + 48))
        str.append(chr(((v[4 * l + 3] >> 24) & 0x3f) + 48))

        str.append(chr((((v[4 * l + 0] >> 30) & 0x01) |
                          ((v[4 * l + 1] >> 29) & 0x02) |
                          ((v[4 * l + 2] >> 28) & 0x04) |
                          ((v[4 * l + 3] >> 27) & 0x08)) + 48))

    print(''.join(str))

if __name__ == "__main__":
    main()