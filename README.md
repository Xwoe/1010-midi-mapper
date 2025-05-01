# 1010-midi-mapper
A tool to transfer MIDI mappings from one project to multiple other project.



### Run the whole chain locally for blackbox presets
Make all shell scripts in the folder executable:
```bash
chmod +x *.sh
```
 ```bash
 ./process_blackbox.sh -i "./test_files/blackbox/XWOEAGAIN 10 A203" -o "./test_files/blackbox"
 ```



## Example usage `copy_blackbox.sh`

Make all shell scripts in the folder executable:
```bash
chmod +x *.sh
```
Run it with the test files included in this repository.

 ```bash
 ./copy_blackbox.sh -i "./test_files/blackbox/XWOEAGAIN 10 A203" -o "./test_files/blackbox"
 ```