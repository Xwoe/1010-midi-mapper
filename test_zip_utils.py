import os
import unittest
import filecmp
from tenten_zip_utils import zip_folder_to_memory, unzip_files


class TestZipUtils(unittest.TestCase):
    def test_zip_unzip(self):
        # Zip the files in outfolder
        zip_buffer = zip_folder_to_memory(self.outfolder)

        # Write the zip buffer to a file
        with open(self.zip_output_path, "wb") as f:
            f.write(zip_buffer.getvalue())

        # Unzip the file to the unzip_output_folder
        unzip_files(self.zip_output_path, self.unzip_output_folder)

        # Verify the contents of the extracted folder match the original folder
        comparison = filecmp.dircmp(self.outfolder, self.unzip_output_folder)
        self.assertEqual(len(comparison.left_only), 0, "Extra files in original folder")
        self.assertEqual(
            len(comparison.right_only), 0, "Extra files in extracted folder"
        )
        self.assertEqual(
            len(comparison.diff_files), 0, "Mismatched files between folders"
        )

    def setUp(self):
        self.outfolder = "./test_files/outfolder"
        self.zip_output_path = "./test_files/test_output.zip"
        self.unzip_output_folder = "./test_files/test_zip_output"

        # Ensure the required directories exist
        if not os.path.exists(self.outfolder):
            self.skipTest(f"Required folder '{self.outfolder}' does not exist.")
        os.makedirs("./test_files", exist_ok=True)

    def tearDown(self):
        # Clean up test files and directories
        if os.path.exists(self.zip_output_path):
            os.remove(self.zip_output_path)
        if os.path.exists(self.unzip_output_folder):
            for root, _, files in os.walk(self.unzip_output_folder, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                os.rmdir(root)
