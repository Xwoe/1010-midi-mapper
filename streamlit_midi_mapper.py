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

if "preset_uploaded" not in st.session_state:
    st.session_state["preset_uploaded"] = False

if "disable_preset_upload" not in st.session_state:
    st.session_state["disable_preset_upload"] = False

if "disable_outfile_upload" not in st.session_state:
    st.session_state["disable_outfile_upload"] = False

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


def cleanup_temp_folder():
    """
    Cleans up the temporary folder created for file uploads.
    """
    # if st.session_state["temp_folder"] is not None:
    #     st.session_state["uploaded_preset"] = None
    #     st.session_state["uploaded_outfiles"] = None
    #     st.session_state["preset_uploaded"] = False
    st.session_state["temp_folder"].cleanup()
    # st.session_state["temp_folder"] = None


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


st.markdown(
    """
    ## 1 Select your device
    Select the device you want to map.
    """
)


def onselectbox_change():
    st.session_state["preset_uploaded"] = False
    st.session_state["uploaded_outfiles"] = None
    st.session_state["mm"].reset()


st.session_state["device"] = st.selectbox(
    label="Select your device",
    options=[
        "blackbox",
        "lemondrop",
        "genericnanobox",
    ],
    index=None,
    disabled=st.session_state["preset_uploaded"],
)

######################################
# Upload Template
######################################

if st.session_state["device"] is not None:
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
        disabled=st.session_state["zip_output"] is not None,
    )
    if (
        st.session_state["uploaded_preset"] is not None
        and not st.session_state["disable_preset_upload"]
    ):
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

        st.session_state["disable_preset_upload"] = True

######################################
# 3 Upload Target Files
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
        disabled=st.session_state["zip_output"] is not None,
    )
    if (
        st.session_state["uploaded_outfiles"] is not None
        and st.session_state["disable_outfile_upload"] is False
    ):
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
                st.session_state["mm"].add_outfile(temp_file.name)
        if len(st.session_state["mm"].outfiles) > 0:
            st.session_state["disable_outfile_upload"] = True


######################################
# 4 Settings
######################################
if st.session_state["uploaded_outfiles"] is not None:
    st.markdown(
        """
    ## 4 Select your settings
    Select the settings you want to transfer.
    """
    )
    st.checkbox(
        "Wipe all existing CC mappings",
        value=False,
        disabled=st.session_state["zip_output"] is not None,
    )
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
                disabled=st.session_state["zip_output"] is not None,
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
                disabled=st.session_state["zip_output"] is not None,
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
        disabled=st.session_state["zip_output"] is not None,
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
            st.session_state["zip_out_name"] = (
                f"{st.session_state['device']}_mapped_files.zip"
            )
            st.session_state["zip_output"] = zip_files_to_memory(
                file_list=result_files, zipfile_name=st.session_state["zip_out_name"]
            )
            st.success("Mapping completed successfully.")
            cleanup_temp_folder()

        except Exception as e:
            st.error(f"Error during mapping: {e}")
            cleanup_temp_folder()


######################################
# 5 Download Button
######################################
if st.session_state["zip_output"] is not None:

    st.markdown(
        """
    ## 5 Download your mapped files
    """
    )

    st.download_button(
        label="Download mapped files",
        data=st.session_state["zip_output"],
        file_name=st.session_state["zip_out_name"],
        mime="application/zip",
        use_container_width=True,
    )
