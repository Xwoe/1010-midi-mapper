#!/bin/bash

# Parse command-line arguments
while getopts "i:o:r" opt; do
  case $opt in
    i) infile="$OPTARG" ;;
    o) outfolder="$OPTARG" ;;
    r) replace="--replace" ;;
    *) echo "Usage: $0 -i <input_file> -o <output_folder> [-r]"; exit 1 ;;
  esac
done

# Check if required arguments are provided
if [ -z "$infile" ] || [ -z "$outfolder" ]; then
  echo "Usage: $0 -i <input_file> -o <output_folder> [-r]"
  exit 1
fi

# Call the midi_mapper.py script with the provided arguments
python3 midi_mapper.py -i "$infile" -o "$outfolder" -t blackbox $replace
