#!/bin/bash

# Check if input file is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <input_kml_file>"
  exit 1
fi

# Input file path from the first argument
input_file="$1"

# Use awk to extract and format all coordinates in the file
awk '
    BEGIN { FS="<coordinates>|</coordinates>" }
    {
        # Loop over all possible <coordinates> ... </coordinates> sets in a line
        while (match($0, /<coordinates>[^<]*<\/coordinates>/)) {
            coords_str = substr($0, RSTART + 13, RLENGTH - 27);
            gsub(/ /, "\n", coords_str);  # Replace space with newline for each coordinate pair

            # Process each coordinate pair
            n = split(coords_str, coords, "\n");
            for (i = 1; i <= n; i++) {
                split(coords[i], parts, ",");
                if (length(parts[1]) > 0 && length(parts[2]) > 0) {
                    print parts[1], parts[2];  # Print longitude and latitude
                }
            }

            # Remove processed part from the line
            $0 = substr($0, RSTART + RLENGTH);
        }
    }
' "$input_file"
