import unittest

from midi_mapper import MidiMapper
import models


class TestBlackbox(unittest.TestCase):
    def test_blackbox_all_settings(self):
        bsettings = models.BlackboxSettings(
            pad_params=[
                models.BlackboxPadParam.MIDIMODE,
                models.BlackboxPadParam.OUTPUT_BUS,
            ],
            noteseq_params=[
                models.BlackboxNoteseqParam.SEQPADMAPDEST,
                models.BlackboxNoteseqParam.MIDIOUTCHAN,
                models.BlackboxNoteseqParam.MIDISEQCELLCHAN,
            ],
        )
        infile = "./test_files/blackbox/XWOEAGAIN 10 A203/preset.xml"
        outfiles = [
            "./test_files/blackbox/SL AMBIENT DRONES/preset.xml",
            "./test_files/blackbox/SL BASS MUSIC KIT/preset.xml",
            "./test_files/blackbox/SL DARK AMBIENT/preset.xml",
        ]
        mm = MidiMapper(
            infile=infile,
            outfiles=outfiles,
            tenten_device=models.TenTenDevice.BLACKBOX,
            settings=bsettings,
        )
        mm.run()
        # TODO add some actual tests

    def test_mismatch(self):
        bsettings = models.BlackboxSettings(
            pad_params=[
                models.BlackboxPadParam.MIDIMODE,
                models.BlackboxPadParam.OUTPUT_BUS,
            ],
            noteseq_params=[
                models.BlackboxNoteseqParam.SEQPADMAPDEST,
                models.BlackboxNoteseqParam.MIDIOUTCHAN,
                models.BlackboxNoteseqParam.MIDISEQCELLCHAN,
            ],
        )
        infile = "./test_files/blackbox/XWOEAGAIN 10 A203/preset.xml"
        outfiles = [
            "./test_files/blackbox/SL AMBIENT DRONES/preset.xml",
            "./test_files/blackbox/SL BASS MUSIC KIT/preset.xml",
            ".test_files/blackbox/SL DARK AMBIENT/preset.xml",
        ]

        class RandomClass:
            pass

        self.assertRaises(
            TypeError,
            lambda: MidiMapper(
                infile=infile,
                outfiles=outfiles,
                tenten_device=models.TenTenDevice.BLACKBOX,
                settings=RandomClass(),  # This should cause a mismatch
            ),
        )


class TestLemondrop(unittest.TestCase):
    def test_lemondrop(self): ...
