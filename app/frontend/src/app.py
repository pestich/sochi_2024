import os
import shutil
import tempfile
import uuid
from zipfile import ZipFile

import pandas as pd
import requests
import streamlit as st

from menu import main_menu

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())


st.sidebar.write(f"ID сессии: {st.session_state['session_id']}")

st.sidebar.write("\n")

main_menu()
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("\n")

st.title("📄Команда MaDS: Семантическая классификация документов")


