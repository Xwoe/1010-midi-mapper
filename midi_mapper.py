#!/usr/bin/env python3

import os
import uuid
import sys
import argparse

from lxml import etree
from copy import copy

from mod_source_list import NUM_SLOTS, ModSourceList

# import models
from models import (
    BlackboxSettings,
    BlackboxPadParam,
    BlackboxNoteseqParam,
    TenTenDevice,
)

ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))

DEFAULT_SLOT = "1"

PADPARAM_DEVICES = [TenTenDevice.BLACKBOX]
NOTESEQ_PARAM_DEVICES = [TenTenDevice.BLACKBOX]


class MidiMapper:
    def __init__(
        self,
        infile: str = "",
        outfiles: list = [],
        overwrite_files: bool = False,
        wipe_existing_mappings: bool = False,
        tenten_device=TenTenDevice.BLACKBOX,
        settings=None,
    ):
        self.infile = infile
        self.outfiles = outfiles
        self.overwrite_files = overwrite_files
        self.wipe_existing_mappings = wipe_existing_mappings
        self.tenten_device = tenten_device
        self.settings = settings
        self.parser = etree.XMLParser(recover=True)
        self.root_infile = None
        self.result_files = []

    def prepare_data(self):
        self.outfiles = self.filter_outfiles(self.outfiles)
        self.check_settings()
        self.read_preset_file(self.infile)
        self.modsources_infile = self.filter_midi_modsources(self.root_infile)
        self.pad_params_infile = self.filter_pad_params(self.root_infile)
        self.noteseq_params_infile = self.filter_noteseq_params(self.root_infile)
        self.outfile_subfolder = self.get_output_folder()

    def read_preset_file(self, file_path: str):
        if self.root_infile is None:
            self.root_infile = self.read_xml_file(file_path)

    def filter_outfiles(self, outfiles):
        if len(outfiles) == 0:
            raise ValueError("No output files provided.")
        return [f for f in outfiles if not f == self.infile]

    def check_settings(self):
        # make sure the settings have been passed correctly
        if self.tenten_device == TenTenDevice.BLACKBOX:
            if not isinstance(self.settings, BlackboxSettings):
                raise TypeError(
                    "Settings must be of type BlackboxSettings for BLACKBOX device."
                    + f" Got {type(self.settings)} instead."
                )

        else:
            return

    def get_output_folder(self):
        try:
            outfiles_basefolder = os.path.dirname(self.outfiles[0])
        except IndexError:
            raise ValueError("No output files provided.")
        if self.overwrite_files:
            return os.path.abspath(os.path.join(outfiles_basefolder, ".."))
        # generate a randomly named sub folder as the output
        folder = os.path.abspath(
            os.path.join(outfiles_basefolder, "..", str(uuid.uuid4())[:8])
        )
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    def read_xml_file(self, filepath):
        with open(filepath, "rb") as f:
            xml = f.read()
            root = etree.fromstring(xml, parser=self.parser)
            return root

    def run(self):
        self.prepare_data()
        for outfile in self.outfiles:
            root_outfile = self.read_xml_file(outfile)
            self.wipe_modsources(root_outfile)
            self.insert_modsources(root_outfile)
            self.insert_pad_params(root_outfile)
            self.insert_noteseq_params(root_outfile)
            result_file = self.write_xml_file(filepath=outfile, root=root_outfile)
            self.result_files.append(result_file)
        return self.result_files

    def filter_midi_modsources(self, root):
        modsources = root.xpath('.//modsource[@src="midicc"]')
        return modsources

    def filter_pad_params(self, root):
        padparams = root.xpath('.//cell[@type="sample"]/params')
        return padparams

    def filter_noteseq_params(self, root):
        noteseqparams = root.xpath('.//cell[@seqsublayer="0"][@type="noteseq"]/params')
        return noteseqparams

    def wipe_modsources(self, root_outfile):
        if not self.wipe_existing_mappings:
            return
        # remove all modsources from the outfile
        modsources = root_outfile.xpath('.//modsource[@src="midicc"]')
        for modsource in modsources:
            self.delete_modsource(modsource)

    def delete_modsource(self, modsource):
        parent = modsource.getparent()
        parent.remove(modsource)

    def insert_modsources(self, root_outfile):
        for mod_infile in self.modsources_infile:
            # get element from infile
            parent_attrib_infile = mod_infile.getparent().attrib
            # get cell from outfile at the same position
            cell_outfile = root_outfile.xpath(
                f'.//cell[@row="{parent_attrib_infile["row"]}"][@column="{parent_attrib_infile["column"]}"]'
            )
            try:
                cell_outfile = cell_outfile[0]
            except IndexError:
                print(
                    f"Cell not found in outfile for row {parent_attrib_infile['row']} and column {parent_attrib_infile['column']}"
                )
                continue
            # get all modsources from the outfile, which have the same destination
            modsources = cell_outfile.xpath(
                f'./modsource[@dest="{mod_infile.attrib["dest"]}"]'
            )
            mod_same_dest = ModSourceList(modsources=modsources)

            # if there is a free slot, we will place it there
            first_free_slot = mod_same_dest.first_free_slot()
            if first_free_slot is not None:
                # place it in the first free slot
                self.add_to_free_slot(mod_infile, cell_outfile, first_free_slot)
                continue

            # if there is a midicc modsource, we will replace it
            first_cc_modsource = mod_same_dest.first_cc_modsource()
            if first_cc_modsource is not None:
                slot = first_cc_modsource.attrib["slot"]
                self.delete_modsource(first_cc_modsource)
                self.add_to_free_slot(mod_infile, cell_outfile, slot)
                continue

            # if there is no gap and no cc slot, we will replace the middle one with index 1
            # (because in blackbox 0 and 2 are sometimes set by default)
            middle_elem = mod_same_dest.elem_at_slot(DEFAULT_SLOT)
            if middle_elem is not None:
                self.delete_modsource(middle_elem)

            # create a new one
            new_elem = copy(mod_infile)
            new_elem.attrib["slot"] = DEFAULT_SLOT
            cell_outfile.append(new_elem)

    def insert_pad_params(self, root_outfile):
        if not self.tenten_device in PADPARAM_DEVICES:
            return
        for pad_params in self.pad_params_infile:
            try:
                pad_params_cell = pad_params.getparent()
                # get element from outfile
                params_outfile = root_outfile.xpath(
                    f'.//cell[@row="{pad_params_cell.attrib["row"]}"]'
                    + f'[@column="{pad_params_cell.attrib["column"]}"]'
                    + f'[@layer="{pad_params_cell.attrib["layer"]}"]/params'
                )
                params_outfile = params_outfile[0]
                for key in self.settings.pad_params:
                    if key in pad_params.attrib:
                        params_outfile.attrib[key] = pad_params.attrib[key]

            except IndexError:
                print(
                    f"Cell not found in outfile for row {pad_params.attrib['row']} and column {pad_params.attrib['column']}"
                )
                continue

            except Exception as e:
                print(f"Error: {e}")
                continue

    def insert_noteseq_params(self, root_outfile):
        if not self.tenten_device in NOTESEQ_PARAM_DEVICES:
            return
        for noteseq_params in self.noteseq_params_infile:
            try:
                noteseq_params_cell = noteseq_params.getparent()

                # get element from outfile

                params_outfile = root_outfile.xpath(
                    f'.//cell[@row="{noteseq_params_cell.attrib["row"]}"]'
                    + f'[@column="{noteseq_params_cell.attrib["column"]}"]'
                    + f'[@layer="{noteseq_params_cell.attrib["layer"]}"]'
                    + f'[@seqsublayer="{noteseq_params_cell.attrib["seqsublayer"]}"]/params'
                )
                # it might be that the sequence hasn't been initialized yet and in that case
                # the seqsublayer is empty
                if not params_outfile:
                    params_outfile = root_outfile.xpath(
                        f'.//cell[@row="{noteseq_params_cell.attrib["row"]}"]'
                        + f'[@column="{noteseq_params_cell.attrib["column"]}"]'
                        + f'[@layer="{noteseq_params_cell.attrib["layer"]}"]/params'
                    )

                params_outfile = params_outfile[0]
                for key in self.settings.noteseq_params:
                    if key in noteseq_params.attrib:
                        params_outfile.attrib[key] = noteseq_params.attrib[key]

            except IndexError:
                print(
                    f"Cell not found in outfile for row {noteseq_params_cell.attrib['row']} "
                    + f"and column {noteseq_params_cell.attrib['column']}"
                )
                continue

            except Exception as e:
                print(f"Error: {e}")
                continue

    def add_to_free_slot(self, mod_infile, cell_outfile, slot):
        new_elem = copy(mod_infile)
        new_elem.attrib["slot"] = slot
        cell_outfile.append(new_elem)

    def add_outfile(self, outfile):
        self.outfiles.append(outfile)

    def write_xml_file(self, filepath, root):
        if self.overwrite_files:
            new_fp = filepath
        else:
            # get the filename and prepare the output path
            file_name = os.path.basename(filepath)

            base_name, file_extension = os.path.splitext(file_name)
            new_fp = os.path.join(self.outfile_subfolder, file_name)

            # handle filename conflicts by appending an incrementing index
            index = 1
            while os.path.exists(new_fp):
                new_fp = os.path.join(
                    self.outfile_subfolder, f"{base_name}{index}{file_extension}"
                )
                index += 1

        with open(new_fp, "wb") as f:
            xml = etree.tostring(
                root,
                pretty_print=True,
                encoding="UTF-8",
                xml_declaration=True,
            )
            f.write(xml)

        return new_fp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the MIDI Mapper.")
    parser.add_argument("-i", "--infile", required=True, help="Input file path")
    parser.add_argument("-o", "--outfolder", required=True, help="Output folder path")
    parser.add_argument(
        "-t",
        "--tenten_device",
        required=True,
        choices=["lemondrop", "blackbox"],
        help="TenTen device type (lemondrop or blackbox)",
    )
    parser.add_argument(
        "-r",
        "--replace",
        action="store_true",
        help="Replace existing files in the output folder",
    )

    args = parser.parse_args()

    infile = args.infile
    outfolder = args.outfolder
    tenten_device = args.tenten_device
    overwrite = args.replace

    # Validate infile
    if not os.path.isfile(infile):
        print(f"Error: Infile '{infile}' does not exist.")
        sys.exit(1)

    # Validate outfolder
    if not os.path.exists(outfolder):
        print(f"Error: Outfolder '{outfolder}' does not exist.")
        sys.exit(1)

    # Collect all .xml files in the outfolder and its subdirectories
    outfiles = []
    for root, _, files in os.walk(outfolder):
        for file in files:
            if file.endswith(".xml"):
                outfiles.append(os.path.join(root, file))

    if not outfiles:
        print(f"Error: No .xml files found in the outfolder '{outfolder}'.")
        sys.exit(1)

    # Set device-specific settings
    if tenten_device == "blackbox":
        settings = BlackboxSettings(
            pad_params=[
                BlackboxPadParam.MIDIMODE,
                BlackboxPadParam.OUTPUTBUS,
            ],
            noteseq_params=[
                BlackboxNoteseqParam.SEQPADMAPDEST,
                BlackboxNoteseqParam.MIDIOUTCHAN,
                BlackboxNoteseqParam.MIDISEQCELLCHAN,
            ],
        )
        device = TenTenDevice.BLACKBOX
    elif tenten_device == "lemondrop":
        settings = None
        device = TenTenDevice.LEMONDROP

    # Run the MidiMapper
    mm = MidiMapper(
        infile=infile,
        outfiles=outfiles,
        tenten_device=device,
        settings=settings,
        overwrite_files=overwrite,
    )
    mm.run()
    if overwrite:
        print(f"Processing completed. Output files replaced in '{outfolder}'.")
    else:
        print(
            f"Processing completed. Output files written to '{mm.outfile_subfolder}'."
        )
