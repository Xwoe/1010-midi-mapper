#!/bin/bash

# Check if a folder is provided as an argument
if [ $# -eq 0 ]; then
  echo "Usage: $0 <folder>"
  exit 1
fi

root_folder="$1"

# Check if the provided folder exists
if [ ! -d "$root_folder" ]; then
  echo "Error: Folder '$root_folder' does not exist."
  exit 1
fi

# Iterate over subfolders
for subfolder in "$root_folder"/*/; do
  # Check if the subfolder contains a preset.xml file
  preset_file="$subfolder/preset.xml"
  if [ ! -f "$preset_file" ]; then
    echo "Skipping '$subfolder': No preset.xml file found."
    continue
  fi

  echo "Processing folder: $subfolder"

  # Extract all referenced filenames from the preset.xml
  referenced_files=$(grep -o 'filename="\.\\[^"]\+"' "$preset_file" | sed 's/filename="\.\\//g' | sed 's/"//g')

  # Iterate over all .wav files in the subfolder
  for wav_file in "$subfolder"*.wav; do
    # Skip if no .wav files are found
    if [ ! -f "$wav_file" ]; then
      continue
    fi

    # Get the base name of the .wav file
    wav_basename=$(basename "$wav_file")

    # Check if the .wav file is referenced in the preset.xml
    if ! echo "$referenced_files" | grep -q "^$wav_basename$"; then
      echo "Deleting unreferenced file: $wav_file"
      rm "$wav_file"
    fi
  done
done
