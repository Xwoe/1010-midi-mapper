import io
import os
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


def clean_up_filename(file_path):
    """
    Cleans up the filename by removing the extension and replacing spaces with underscores.
    """
    # Remove the file extension
    file_name = file_path.split("/")[-1]
    # remove the random bit before the file extension and after the .
    parts = file_name.split(".")
    try:
        parts.pop(-2)
        file_name = ".".join(parts)
        return file_name

    except IndexError:
        return file_name


def zip_files_to_memory(file_list, cleanup=False):
    """
    Zips all files in file_list into a single zip file in memory.

    Args:
        file_list (list): List of file paths to include in the zip.
        zipfile_name (str): Name of the zip file.

    Returns:
        BytesIO: A BytesIO object containing the zip file.
    """
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_list:
            with open(file_path, "rb") as f:
                file_data = f.read()
                if cleanup:
                    file_name = clean_up_filename(file_path)
                else:
                    file_name = file_path.split("/")[-1]
                zipf.writestr(file_name, file_data)

    zip_buffer.seek(0)
    return zip_buffer


def unzip_files(zip_name, extract_to, file_extension=None):
    """
    Unzips the zip file zip_name into the directory extract_to.
    There it looks for files with the given file_extension and returns their paths.
    """
    with zipfile.ZipFile(zip_name, "r") as zipf:
        zipf.extractall(extract_to)

    # If a file extension is provided, collect all the files in all subolders with that extension
    # and return their file paths
    if file_extension:
        # get a list of all files with the given extension in all subfolders of extract_to
        # and return their file paths
        file_paths = []
        for root, _, files in os.walk(extract_to):
            for file in files:
                if "__MACOSX" in file:
                    continue
                if file.endswith(file_extension):
                    file_paths.append(os.path.join(root, file))
        return file_paths


def zip_folder_to_memory(folder_path):
    """
    Zips all files inside a folder, maintaining the folder structure, and writes the resulting zip file to an io.BytesIO.

    Args:
        folder_path (str): Path to the folder to zip.

    Returns:
        BytesIO: A BytesIO object containing the zip file.
    """
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    zipf.writestr(os.path.relpath(file_path, folder_path), file_data)

    zip_buffer.seek(0)
    return zip_buffer
