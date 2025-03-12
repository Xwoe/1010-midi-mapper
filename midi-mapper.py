from lxml import etree

INFILE = "/Users/schwoe/DEV/1010-midi-mapper/test_files/NuDefault.nnl"


def read_xml_file(infile):
    with open(infile, "rb") as f:
        return f.read()


def filter_midi_modsources(root):
    # TODO this query doesn't work: "session/cell/modsource[@src='midicc']"
    # modsources = root.xpath("session/cell/modsource")
    modsources = root.xpath('.//modsource[@src="midicc"]')
    return modsources


if __name__ == "__main__":
    xml = read_xml_file(INFILE)
    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(xml, parser=parser)
    modsources = filter_midi_modsources(root)
    # parent, where to insert them
    # el.getparent().attrib
    # modsource element to replace el.attrib["dest"]
    # if there are three modsources for the same dest, we have to replace one of them
    # by default write it at the first free position if not free, replace the last one

    print(modsources)
