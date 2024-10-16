#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <input_kml_file>"
  exit 1
fi

input_file="$1"

awk '
    BEGIN { FS="<coordinates>|</coordinates>" }
    {
        while (match($0, /<coordinates>[^<]*<\/coordinates>/)) {
            coords_str = substr($0, RSTART + 13, RLENGTH - 27);
            split(coords_str, coords, " ");
            split(coords[1], parts, ",");
            if (length(parts[1]) > 0 && length(parts[2]) > 0) {
                print parts[1], parts[2];
            }
            $0 = substr($0, RSTART + RLENGTH);
        }
    }
' "$input_file"
