import os
import streamlit as st
from tempfile import NamedTemporaryFile, TemporaryDirectory, TemporaryFile
from pathlib import Path
from io import StringIO
from tenten_zip_utils import zip_files_to_memory, unzip_files

from midi_mapper import MidiMapper
from models import (
    TENTEN_EXTENSIONS,
    BlackboxSettings,
    BlackboxPadParam,
    BlackboxNoteseqParam,
    BB_PAD_PARAM_DESCRIPTION,
    BB_NOTESEQ_PARAM_DESCRIPTION,
)


######################################
# Initialize session state variables
if "mm" not in st.session_state:
    st.session_state["mm"] = MidiMapper()
if "uploaded_preset" not in st.session_state:
    st.session_state["uploaded_preset"] = None
if "uploaded_outfiles" not in st.session_state:
    st.session_state["uploaded_outfiles"] = None
if "temp_folder" not in st.session_state:
    st.session_state["temp_folder"] = TemporaryDirectory(
        suffix="",
        prefix="tenten_folder_",
        delete=False,
    )
if "device" not in st.session_state:
    st.session_state["device"] = None

if "file_extension" not in st.session_state:
    st.session_state["file_extension"] = None

if "wipe_existing_mappings" not in st.session_state:
    st.session_state["wipe_existing_mappings"] = False

# Blackbox Pad Params
for key in BlackboxPadParam:
    if key not in st.session_state:
        st.session_state[key] = False

# Blackbox Noteseq Params
for key in BlackboxNoteseqParam:
    if key not in st.session_state:
        st.session_state[key] = False

if "zip_output" not in st.session_state:
    st.session_state["zip_output"] = None
# st.write(st.session_state["temp_folder"].name)


######################################
# Title
######################################
st.title("Midi and Preset Mapper for 1010music Devices")
st.caption("by [Xwoe](https://github.com/Xwoe/1010-midi-mapper)")
st.markdown(
    """
    ### TODO
    """
)

######################################
# Device Selection
######################################
st.session_state["preset_uploaded"] = False

st.markdown(
    """
    ## 1 Select your device
    Select the device you want to map.
    """
)
st.session_state["device"] = st.selectbox(
    label="Select your device",
    options=[
        "blackbox",
        "lemondrop",
        "genericnanobox",
    ],
    index=0,
)

######################################
# Upload Template
######################################
st.markdown(
    """
    ## 2 Upload your "template" file
    Upload the file, which contains all the midi mappings and settings you want to transfer to other presets.
    """
)
st.session_state["uploaded_preset"] = st.file_uploader(
    "Choose a file",
    type=[
        TENTEN_EXTENSIONS[st.session_state["device"]],
    ],
)
if st.session_state["uploaded_preset"] is not None:
    suffix = Path(st.session_state["uploaded_preset"].name).suffix

    with NamedTemporaryFile(
        suffix=suffix,
        prefix=st.session_state["uploaded_preset"].name,
        delete=False,
        delete_on_close=False,
        dir=st.session_state["temp_folder"].name,
    ) as temp_file:
        temp_file.write(st.session_state["uploaded_preset"].getvalue())
        temp_file.seek(0)
        st.session_state["mm"].read_preset_file(temp_file.name)
        st.session_state["preset_uploaded"] = True


######################################
# Upload Target Files
######################################
if st.session_state["preset_uploaded"]:
    st.markdown(
        """
    ## 3 Upload your "target" files
    Upload the files, to which you want to map the settings from the template.
    """
    )
    st.session_state["uploaded_outfiles"] = st.file_uploader(
        "Choose a file",
        type=[
            TENTEN_EXTENSIONS[st.session_state["device"]],
        ],
        accept_multiple_files=True,
    )
    if st.session_state["uploaded_outfiles"] is not None:
        for uploaded_file in st.session_state["uploaded_outfiles"]:
            suffix = Path(uploaded_file.name).suffix

            with NamedTemporaryFile(
                suffix=suffix,
                prefix=uploaded_file.name,
                delete=False,
                delete_on_close=False,
                dir=st.session_state["temp_folder"].name,
            ) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file.seek(0)
                st.session_state["mm"].read_preset_file(temp_file.name)
                st.session_state["mm"].add_outfile(temp_file.name)


######################################
# Settings
######################################
if st.session_state["preset_uploaded"]:
    st.markdown(
        """
    ## 4 Select your settings
    Select the settings you want to transfer.
    """
    )
    st.checkbox("Wipe all existing CC mappings", value=False)
    if st.session_state["device"] == "blackbox":
        st.markdown(
            """
            ### Blackbox Pad Parameters
        """
        )
        for key in BlackboxPadParam:
            st.session_state[key] = st.checkbox(
                BB_PAD_PARAM_DESCRIPTION.get(key),
                value=True,
            )

        st.markdown(
            """
            ### Blackbox Sequence Parameters
            """
        )
        for key in BlackboxNoteseqParam:
            st.session_state[key] = st.checkbox(
                BB_NOTESEQ_PARAM_DESCRIPTION.get(key),
                value=True,
            )


def read_settings():
    st.write("device: ", st.session_state["device"])
    if st.session_state["device"] == "blackbox":
        bb_settings = BlackboxSettings()
        bb_settings.pad_params = [
            key for key in BlackboxPadParam if st.session_state[key]
        ]
        bb_settings.noteseq_params = [
            key for key in BlackboxNoteseqParam if st.session_state[key]
        ]

        return bb_settings
    else:
        st.write("No settings available for this device.")
        return None


######################################
# Run Mapping
######################################

if st.session_state["uploaded_outfiles"] is not None:
    opti_label = "Transfer Preset Settings"
    if st.button(
        label=opti_label,
        type="primary",
        use_container_width=False,
    ):
        try:
            st.session_state["mm"].overwrite_files = True
            st.session_state["mm"].wipe_existing_mappings = st.session_state[
                "wipe_existing_mappings"
            ]
            st.session_state["mm"].tenten_device = st.session_state["device"]
            st.session_state["mm"].settings = read_settings()
            result_files = st.session_state["mm"].run()
            # TODO read zip file to memory and make downloadable
            st.session_state["zip_output"] = zip_files_to_memory(result_files)
            st.success("Mapping completed successfully.")
            st.session_state["temp_folder"].cleanup()

        except Exception as e:
            st.error(f"Error during mapping: {e}")
            st.session_state["temp_folder"].cleanup()
