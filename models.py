from pydantic import BaseModel, Field
from enum import Enum


class TenTenDevice(str, Enum):
    BLACKBOX = "blackbox"
    LEMONDROP = "lemondrop"
    # GENERICNANOBOX = "genericnanobox"


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
    BlackboxNoteseqParam.SEQPADMAPDEST: "Seq pad map destination",
    BlackboxNoteseqParam.MIDIOUTCHAN: "MIDI out channel",
    BlackboxNoteseqParam.MIDISEQCELLCHAN: "MIDI seq cell channel",
}


class BlackboxSettings(BaseModel):
    pad_params: list = Field(default_factory=list)
    noteseq_params: list = Field(default_factory=list)


TENTEN_EXTENSIONS = {
    "blackbox": "xml",
    "lemondrop": "nnl",
    # "genericnanobox": "*",
}
