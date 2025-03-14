from lxml import etree

INFILE = "/Users/schwoe/DEV/1010-midi-mapper/test_files/NuDefault.nnl"
OUTFILES = ["/Users/schwoe/DEV/1010-midi-mapper/test_files/TEST MAPPING.nnl"]


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
            mod_same_dest = cell_outfile[0].xpath(
                f'./modsource[@dest="{mod_infile.attrib["dest"]}"]'
            )
            if len(mod_same_dest) == 0:
                # place it in the first slot
                ...
            # if there are there are modsources, we will first look for the ones with midicc.
            # if there is one we will replace it
            # if there is a gap... slot 0, 1 or 2 not filled, we will place it there
            # if there is no gap, we will replace the middle one with index 1 (because in blackbox 0 and 2 are sometimes set by default)

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
