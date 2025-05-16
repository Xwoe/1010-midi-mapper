from pydantic import BaseModel, Field
from enum import Enum


class TenTenDevice(str, Enum):
    BLACKBOX = "blackbox"
    LEMONDROP = "lemondrop"
    FIREBALL = "fireball"
    RAZZMATAZZ = "razzmatazz"
    TANGERINE = "tangerine"


class BlackboxPadParam(str, Enum):
    MIDIMODE = "midimode"
    OUTPUTBUS = "outputbus"


class ModSources(str, Enum):
    MIDICC = "midicc"
    VELOCITY = "velocity"
    MIDIVOLUME = "midivol"
    MIDIPAN = "midipan"
    MODWHEEL = "modwheel"
    PITCHBEND = "pitchbend"


DISPLAY_NAMES = {
    BlackboxPadParam.MIDIMODE: "MIDI mode",
    BlackboxPadParam.OUTPUTBUS: "Output bus",
    ModSources.MIDICC: "MIDI CC",
    ModSources.VELOCITY: "Velocity",
    ModSources.MIDIVOLUME: "MIDI Volume",
    ModSources.MIDIPAN: "MIDI Pan",
    ModSources.MODWHEEL: "Mod Wheel",
    ModSources.PITCHBEND: "Pitch Bend",
}


class BlackboxNoteseqParam(str, Enum):
    SEQPADMAPDEST = "seqpadmapdest"
    MIDIOUTCHAN = "midioutchan"
    MIDISEQCELLCHAN = "midiseqcellchan"


BB_NOTESEQ_PARAM_DESCRIPTION = {
    BlackboxNoteseqParam.SEQPADMAPDEST: "Sequence Pad Destination",
    BlackboxNoteseqParam.MIDIOUTCHAN: "MIDI Out Channel",
    BlackboxNoteseqParam.MIDISEQCELLCHAN: "MIDI Sequence Cell Channel",
}


class BlackboxSettings(BaseModel):
    pad_params: list = Field(default_factory=list)
    noteseq_params: list = Field(default_factory=list)


class GeneralMidiSettings(BaseModel):
    mod_sources: list = Field(default_factory=list)


TENTEN_EXTENSIONS = {
    "blackbox": "xml",
    "lemondrop": "nnl",
    "fireball": "nnf",
    "razzmatazz": "nnr",
    "tangerine": "xml",
}

# the products for which we require to upload zip files
TENTEN_ZIP_PRODUCTS = [TenTenDevice.BLACKBOX, TenTenDevice.TANGERINE]

# these products hava block of midi mappings under `midimap` with the
# node names `mapitem`
TENTEN_MIDIMAP_ITEMS = [TenTenDevice.RAZZMATAZZ]

# these products have a cell with the coordinates
# row`, `column` and `layer`
TENTEN_ROW_COLUMN_LAYER = [
    TenTenDevice.BLACKBOX,
    TenTenDevice.TANGERINE,
    TenTenDevice.FIREBALL,
]

# these products have a cell with the coordinates
# row`, `column` and `synth`
TENTEN_ROW_COLUMN_SYNTH = [
    TenTenDevice.RAZZMATAZZ,
    TenTenDevice.LEMONDROP,
]

# checkboxes will be set to false for the keys in this list
DEFAULT_FALSE_CHECKBOX = [
    BlackboxPadParam.OUTPUTBUS,
]
