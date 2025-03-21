from lxml import etree
from copy import copy

INFILE = "/Users/schwoe/DEV/1010-midi-mapper/test_files/NuDefault.nnl"
OUTFILES = ["/Users/schwoe/DEV/1010-midi-mapper/test_files/TEST MAPPING.nnl"]

from mod_source_list import NUM_SLOTS, ModSourceList


DEFAULT_SLOT = "1"


class MidiMapper:
    def __init__(self, infile: str, outfiles: list):
        self.infile = infile
        self.outfiles = outfiles
        self.parser = etree.XMLParser(recover=True)
        self.root_infile = self.read_xml_file(infile)
        self.modsources_infile = self.filter_midi_modsources(self.root_infile)

    def read_xml_file(self, filepath):
        with open(filepath, "rb") as f:
            xml = f.read()
            root = etree.fromstring(xml, parser=self.parser)
            return root

    def filter_midi_modsources(self, root):
        modsources = root.xpath('.//modsource[@src="midicc"]')
        return modsources

    def run(self):
        for outfile in self.outfiles:
            root_outfile = self.read_xml_file(outfile)
            self.insert_modsources(root_outfile)

    def insert_modsources(self, root_outfile):
        for mod_infile in self.modsources_infile:
            # get element from infile
            parent_attrib_infile = mod_infile.getparent().attrib
            # get cell from outfile at the same position
            cell_outfile = root_outfile.xpath(
                f'.//cell[@row="{parent_attrib_infile["row"]}"][@column="{parent_attrib_infile["column"]}"]'
            )
            print(cell_outfile)
            # get all modsources from the outfile, which have the same destination
            modsources = cell_outfile[0].xpath(
                f'./modsource[@dest="{mod_infile.attrib["dest"]}"]'
            )
            mod_same_dest = ModSourceList(modsources=modsources)

            # if there is a free slot, we will place it there
            first_free_slot = mod_same_dest.first_free_slot()
            if first_free_slot:
                # place it in the first free slot
                # TODO don't know if the order matters. Then we would have to find out, what the order of the
                # modsources is in the infile, even if they are missing
                # let's just put it at the end and see if it works. Otherwise we'll have to sort it and
                # add it back in
                new_elem = copy(mod_infile)
                new_elem.attrib["slot"] = first_free_slot
                # TODO probably wrong place to insert it, hast to be appended to the children
                cell_outfile.append(new_elem)
                continue

            # if there is a midicc modsource, we will replace it
            first_cc_modsource = mod_same_dest.first_cc_modsource()
            if first_cc_modsource:
                # replace it
                first_cc_modsource.attrib["mchan"] = mod_infile.attrib["mchan"]
                first_cc_modsource.attrib["cc_num"] = mod_infile.attrib["cc_num"]
                first_cc_modsource.attrib["amount"] = mod_infile.attrib["amount"]
                continue

            # if there is no gap, we will replace the middle one with index 1
            # (because in blackbox 0 and 2 are sometimes set by default)
            middle_elem = mod_same_dest.elem_at_slot(DEFAULT_SLOT)
            if middle_elem:
                # replace it
                middle_elem.attrib["src"] = mod_infile.attrib["src"]
                middle_elem.attrib["mchan"] = mod_infile.attrib["mchan"]
                middle_elem.attrib["cc_num"] = mod_infile.attrib["cc_num"]
                middle_elem.attrib["amount"] = mod_infile.attrib["amount"]
                continue

            # insert element
            # https://stackoverflow.com/questions/68446063/python-lxml-inserting-node-from-one-file-into-another-file-with-proper-structu
            # replace value
            # https://stackoverflow.com/questions/41742435/replacing-a-xml-element-with-lxml


if __name__ == "__main__":

    mm = MidiMapper(infile=INFILE, outfiles=OUTFILES)
    mm.run()
    # parent, where to insert them
    # el.getparent().attrib
    # modsource element to replace el.attrib["dest"]
    # if there are three modsources for the same dest, we have to replace one of them
    # by default write it at the first free position if not free, replace the last one


# https://yasoob.me/2018/06/20/an-intro-to-web-scraping-with-lxml-and-python/
