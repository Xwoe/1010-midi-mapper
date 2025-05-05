import zipfile

from mod_source_list import NUM_SLOTS, ModSourceList
import models


def zip_files(file_list, zip_name):
    """
    Zips the files in file_list into a zip file with the name zip_name.
    """
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for file in file_list:
            zipf.write(file, arcname=file.name)


def unzip_files(zip_name, extract_to):
    """
    Unzips the zip file zip_name into the directory extract_to.
    """
    with zipfile.ZipFile(zip_name, "r") as zipf:
        zipf.extractall(extract_to)
