# 1010-midi-mapper
A tool to transfer MIDI mappings from one project to multiple other project.



### Run the whole chain locally for blackbox presets
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



