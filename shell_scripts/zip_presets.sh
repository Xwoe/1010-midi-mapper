#!/bin/bash

# Check if a folder is provided as an argument
if [ $# -eq 0 ]; then
  echo "Usage: $0 <folder> [filename]"
  exit 1
fi

root_folder="$1"

# Check if the provided folder exists
if [ ! -d "$root_folder" ]; then
  echo "Error: Folder '$root_folder' does not exist."
  exit 1
fi

# Set the filename to search for, defaulting to "preset.xml"
filename="${2:-preset.xml}"

# Create a zip file containing all files matching the filename while preserving local folder structure
zip_file="preset_files.zip"
echo "Creating zip file: $zip_file"
cd "$root_folder" || exit 1
find . -type f -name "$filename" -print | zip -@ "../$zip_file"
cd - > /dev/null

echo "Zip file created: $zip_file"
