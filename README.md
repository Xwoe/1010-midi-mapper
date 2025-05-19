# 1010-midi-mapper
A tool to transfer MIDI mappings from one project to multiple other project.





## Shell Scripts

Some handy shell scripts can be found und `./shell_scripts`


### `blackbox_process.sh`: Run the whole chain locally for blackbox presets
This script will run with the standard settings locally and can optionally overwrite all your `preset.xml` files in place.

Make all the script executable:
```bash
chmod +x blackbox_process.sh
```
To run the processing and put the processed files in a new (randomly named) folder:
 ```bash
 ./blackbox_process.sh -i "./test_files/blackbox/MY AWESOME BB PRESET/preset.xml" -o "./test_files/blackbox"
 ```

 To run the processing and replace the existing files in place:
 ```bash
 ./blackbox_process.sh -i "./test_files/blackbox/MY AWESOME BB PRESET/preset.xml" -o "./test_files/blackbox" -r
 ```

### `zip_presets.sh`: Create a Zip-File Only Containing `preset.xml` Files 
This can be used if you want to use the web tool to convert blackbox projects. It will create a zip file, which only contains the `preset.xml` files, but with the local folder structure. This way you can zip it, upload it, convert it and then extract it over you old files to overwrite only the updated xml files.

Make it executable:
```bash
chmod +x delete_unused_wavs.sh
```
Run it on a folder:
```
./zip_presets.sh /path/to/folder/with/blackbox/projects/
```


### `delete_unused_wavs.sh`: Delete Unused .wav Files
What this does is essentially the same as what would happen if you perform the `clean` operation within the blackbox. It will delete all `.wav` files, which are not referenced in the `preset.xml` file. 

Handle with care as it actually deletes files! Try it with an example folder first.

Make it executable:
```bash
chmod +x delete_unused_wavs.sh
```
Run it on a folder:
```
./delete_unused_wavs.sh /path/to/folder/with/blackbox/projects/
```