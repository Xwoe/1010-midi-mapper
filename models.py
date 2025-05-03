from pydantic import BaseModel, Field
from enum import Enum


class TenTenDevice(str, Enum):
    BLACKBOX = "blackbox"
    LEMONDROP = "lemondrop"
    GENERICNANOBOX = "genericnanobox"


class BlackboxPadParam(str, Enum):
    MIDIMODE = "midimode"
    OUTPUTBUS = "outputbus"


class BlackboxNoteseqParam(str, Enum):
    SEQPADMAPDEST = "seqpadmapdest"
    MIDIOUTCHAN = "midioutchan"
    MIDISEQCELLCHAN = "midiseqcellchan"


class BlackboxSettings(BaseModel):
    pad_params: list = Field(default_factory=list)
    noteseq_params: list = Field(default_factory=list)
