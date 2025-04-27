import os

from lxml import etree
from copy import copy

# INFILE = "/Users/schwoe/DEV/1010-midi-mapper/test_files/lemondrop/NuDefault.nnl"
# OUTFILES = [
#     "/Users/schwoe/DEV/1010-midi-mapper/test_files/lemondrop/TEST MAPPING.nnl",
#     "/Users/schwoe/DEV/1010-midi-mapper/test_files/lemondrop/NAPILI4.nnl",
#     "/Users/schwoe/DEV/1010-midi-mapper/test_files/lemondrop/RHYTHMIC DRONEBIRD.nnl",
# ]

INFILE = "/Users/schwoe/DEV/1010-midi-mapper/test_files/blackbox/XWOEAGAIN 10 A203/preset.xml"
OUTFILES = [
    "/Users/schwoe/DEV/1010-midi-mapper/test_files/blackbox/SL AMBIENT DRONES/preset.xml",
    "/Users/schwoe/DEV/1010-midi-mapper/test_files/blackbox/SL BASS MUSIC KIT/preset.xml",
    "/Users/schwoe/DEV/1010-midi-mapper/test_files/blackbox/SL DARK AMBIENT/preset.xml",
]

from mod_source_list import NUM_SLOTS, ModSourceList


DEFAULT_SLOT = "1"
OUTFILE_APPENDIX_WIPED = "_mm_wiped"
OUTFILE_APPENDIX = "_mm"


class MidiMapper:
    def __init__(
        self,
        infile: str,
        outfiles: list,
        wipe_existing_mappings: bool = False,
        is_copy_cell_params: bool = True,
        is_copy_noteseq_params: bool = True,
    ):
        self.infile = infile
        self.outfiles = outfiles
        self.wipe_existing_mappings = wipe_existing_mappings
        self.parser = etree.XMLParser(recover=True)
        self.root_infile = self.read_xml_file(infile)
        self.is_copy_pad_params = is_copy_cell_params
        self.is_copy_noteseq_params = is_copy_noteseq_params
        self.modsources_infile = self.filter_midi_modsources(self.root_infile)
        self.pad_params_infile = self.filter_pad_params(self.root_infile)
        self.noteseq_params = self.filter_noteseq_params(self.root_infile)

    def read_xml_file(self, filepath):
        with open(filepath, "rb") as f:
            xml = f.read()
            root = etree.fromstring(xml, parser=self.parser)
            return root

    def write_xml_file(self, filepath, root):
        # get the extension of the file
        filename, file_extension = os.path.splitext(filepath)
        appendix = (
            OUTFILE_APPENDIX_WIPED if self.wipe_existing_mappings else OUTFILE_APPENDIX
        )
        new_fp = f"{filename}{appendix}{file_extension}"
        with open(new_fp, "wb") as f:
            xml = etree.tostring(
                root,
                pretty_print=True,
                encoding="UTF-8",
                xml_declaration=True,
            )
            f.write(xml)

    def run(self):
        for outfile in self.outfiles:
            root_outfile = self.read_xml_file(outfile)
            self.wipe_modsources(root_outfile)
            self.insert_modsources(root_outfile)
            self.insert_pad_params(root_outfile)
            self.insert_noteseq_params(root_outfile)
            self.write_xml_file(filepath=outfile, root=root_outfile)

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
                # TODO don't know if the order matters. Then we would have to find out, what the order of the
                # modsources is in the infile, even if they are missing
                # let's just put it at the end and see if it works. Otherwise we'll have to sort it and
                # add it back in
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
        if not self.is_copy_pad_params:
            return
        for pad_params in self.pad_params_infile:
            try:
                pad_params_cell = pad_params.getparent()
                # get element from outfile
                params_outfile = root_outfile.xpath(
                    f'.//cell[@row="{pad_params_cell.attrib["row"]}"][@column="{pad_params_cell.attrib["column"]}"][@layer="{pad_params_cell.attrib["layer"]}"]/params'
                )
                params_outfile = params_outfile[0]
                if "midimode" in pad_params.attrib:
                    params_outfile.attrib["midimode"] = pad_params.attrib["midimode"]

            except IndexError:
                print(
                    f"Cell not found in outfile for row {pad_params.attrib['row']} and column {pad_params.attrib['column']}"
                )
                continue

            except Exception as e:
                print(f"Error: {e}")
                continue

    def insert_noteseq_params(self, root_outfile):
        if not self.is_copy_noteseq_params:
            return
        for noteseq_params in self.noteseq_params:
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
                if "seqpadmapdest" in noteseq_params.attrib:
                    params_outfile.attrib["seqpadmapdest"] = noteseq_params.attrib[
                        "seqpadmapdest"
                    ]
                if "midioutchan" in noteseq_params.attrib:
                    params_outfile.attrib["midioutchan"] = noteseq_params.attrib[
                        "midioutchan"
                    ]
                if "midiseqcellchan" in noteseq_params.attrib:
                    params_outfile.attrib["midiseqcellchan"] = noteseq_params.attrib[
                        "midiseqcellchan"
                    ]

            except IndexError:
                print(
                    f"Cell not found in outfile for row {noteseq_params_cell.attrib['row']} and column {noteseq_params_cell.attrib['column']}"
                )
                continue

            except Exception as e:
                print(f"Error: {e}")
                continue

    def add_to_free_slot(self, mod_infile, cell_outfile, slot):
        new_elem = copy(mod_infile)
        new_elem.attrib["slot"] = slot
        cell_outfile.append(new_elem)

        # insert element
        # https://stackoverflow.com/questions/68446063/python-lxml-inserting-node-from-one-file-into-another-file-with-proper-structu
        # replace value
        # https://stackoverflow.com/questions/41742435/replacing-a-xml-element-with-lxml


if __name__ == "__main__":

    mm = MidiMapper(infile=INFILE, outfiles=OUTFILES)
    # mm = MidiMapper(infile=INFILE, outfiles=OUTFILES, wipe_existing_mappings=True)
    mm.run()
    # parent, where to insert them
    # el.getparent().attrib
    # modsource element to replace el.attrib["dest"]
    # if there are three modsources for the same dest, we have to replace one of them
    # by default write it at the first free position if not free, replace the last one


# https://yasoob.me/2018/06/20/an-intro-to-web-scraping-with-lxml-and-python/


# type noteseq
# seems like we only have to replace the values in seqsublayer="0", because the other seqsublayers never have thos
# value set
# - seqpadmapdest
# - midioutchan
# - midiseqcellchan
