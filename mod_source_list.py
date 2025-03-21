from lxml.etree import Element

NUM_SLOTS = 3
SLOTS = set(["0", "1", "2"])


class ModSourceList:
    def __init__(self, modsources: list):
        self.modsources = modsources

    def first_free_slot(self) -> str:
        occupied_slots = set([m.attrib["slot"] for m in self.modsources])
        set(occupied_slots)
        unoccupied_slots = sorted(SLOTS.difference(occupied_slots))
        if len(unoccupied_slots) == 0:
            return None
        return unoccupied_slots[0]

    def first_cc_modsource(self) -> Element:
        for m in self.modsources:
            if m.attrib["src"] == "midicc":
                return m
        return None

    def insert(self, index: str, modsource: Element):
        self.modsources.insert(int(index), modsource)

    def elem_at_slot(self, slot: str) -> Element:
        for m in self.modsources:
            if m.attrib["slot"] == slot:
                return m
        return None
