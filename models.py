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


BB_PAD_PARAM_DESCRIPTION = {
    BlackboxPadParam.MIDIMODE: "MIDI mode",
    BlackboxPadParam.OUTPUTBUS: "Output bus",
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


TENTEN_EXTENSIONS = {
    "blackbox": "xml",
    "lemondrop": "nnl",
    "fireball": "nnf",
    "razzmatazz": "nnr",
    "tangerine": "xml",
}

# the products for which we require to upload zip files
TENTEN_ZIP_PRODUCTS = [TenTenDevice.BLACKBOX, TenTenDevice.TANGERINE]
