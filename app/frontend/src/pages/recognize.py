import uuid
from urllib.parse import unquote

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


st.title("📚Обработчик документов")


uploaded_file = st.file_uploader(
    "Загрузите файлы в формате pdf, doc, docx или txt",
    type=["pdf", "docx", "txt", "doc"],
    # help="Отсканированные документы НЕ поддерживаются!",
)
add_data = st.button("Отправить")

try:
    if uploaded_file and add_data:
        with st.spinner("Обработка файла..."):
            response = requests.post(
                "http://backend:8000/api/v1/query/upload/single_doc",
                files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)},
                data={"session_id": st.session_state["session_id"]},
            )
            st.text_area(label="Обработанный документ:", value=response.json())


    elif add_data and not uploaded_file:
        st.warning("Добавьте файл для обработки.", icon="⚠️")
except Exception as e:
    st.error("Что-то пошло не так :(", icon="🚨")
    st.error(f"Ошибка: {e}")
