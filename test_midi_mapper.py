import unittest

from midi_mapper import MidiMapper
import models


class TestBlackbox(unittest.TestCase):
    def test_blackbox_all_settings(self):

        general_midi_settings = models.GeneralMidiSettings(
            mod_sources=[
                models.ModSources.MIDICC,
                models.ModSources.VELOCITY,
                models.ModSources.MIDIVOLUME,
                models.ModSources.MIDIPAN,
                models.ModSources.MODWHEEL,
                models.ModSources.PITCHBEND,
            ]
        )
        bsettings = models.BlackboxSettings(
            pad_params=[
                models.BlackboxPadParam.MIDIMODE,
                models.BlackboxPadParam.OUTPUTBUS,
            ],
            noteseq_params=[
                models.BlackboxNoteseqParam.SEQPADMAPDEST,
                models.BlackboxNoteseqParam.MIDIOUTCHAN,
                models.BlackboxNoteseqParam.MIDISEQCELLCHAN,
            ],
        )
        infile = "./test_files/blackbox/XWOEAGAIN 12/preset.xml"
        outfiles = [
            "./test_files/blackbox/MM SL AMBIENT DRONES/preset.xml",
            "./test_files/blackbox/MM SL BASS MUSIC KIT/preset.xml",
            "./test_files/blackbox/MM SL DARK AMBIENT/preset.xml",
        ]
        mm = MidiMapper(
            infile=infile,
            outfiles=outfiles,
            tenten_device=models.TenTenDevice.BLACKBOX,
            device_settings=bsettings,
            general_midi_settings=general_midi_settings,
            overwrite_files=False,
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
                device_settings=RandomClass(),  # This should cause a mismatch
            ),
        )


class TestRazzmatazz(unittest.TestCase):
    def test_razzmatazz_all_settings(self):
        general_midi_settings = models.GeneralMidiSettings(
            mod_sources=[
                models.ModSources.MIDICC,
                models.ModSources.VELOCITY,
                models.ModSources.MIDIVOLUME,
                models.ModSources.MIDIPAN,
                models.ModSources.MODWHEEL,
                models.ModSources.PITCHBEND,
            ]
        )

        infile = "./test_files/razzmatazz/mapped/002BoomClap MIDI V2.nnr"
        outfiles = [
            "./test_files/razzmatazz/mapped/002BoomClap MIDI test.nnr",
            "./test_files/razzmatazz/mapped/002BoomClap.nnr",
            "./test_files/razzmatazz/001AeroVan.nnr",
        ]
        mm = MidiMapper(
            infile=infile,
            outfiles=outfiles,
            tenten_device=models.TenTenDevice.RAZZMATAZZ,
            general_midi_settings=general_midi_settings,
            overwrite_files=False,
        )
        mm.run()
        # TODO add some actual tests
