import os
import shutil
import uuid
from zipfile import ZipFile
import time

import requests
import streamlit as st
import contextlib
from menu import main_menu

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())


st.sidebar.write(f"ID сессии: {st.session_state['session_id']}")

st.sidebar.write("\n")

main_menu()
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("\n")

number = st.sidebar.number_input(
    "Введите количество документов для валидации.",
    value=11,
    placeholder="Введите число...",
)
st.sidebar.write("Текущее число для валидации ", number)


st.title("Загрузка нескольких документов")

file_types = ["pdf", "docx", "txt", "xlsx", "csv"]
uploaded_files = st.file_uploader(
    "Загрузите файлы в формате pdf, docx или txt",
    type=file_types,
    help="Отсканированные документы НЕ поддерживаются!",
    accept_multiple_files=True,
)
add_data = st.button("Отправить документы")





if uploaded_files and add_data:
    with st.spinner("Обработка файла..."):
        all_files = [
            ('files', (file.name, file, file.type)) for file in uploaded_files
        ]
        if len(all_files) == number:
            data = {"session_id": st.session_state["session_id"]}
            response = requests.post(
                "http://backend:8000/api/v1/request/", files=all_files, data=data
            )
            
            if len(response.json()) == 1:
                st.success("Обработка успешно завершена", icon="✅")
            elif len(response.json()) > 1:
                st.warning(
                    "Ошибка валидации. Ниже описание проблемы", icon="⚠️"
                )
            st.write(response.json())
            # st.write(response.content)

        else:
            st.warning(
                "Ошибка валидации. Отправлено неверное количество документов.", icon="⚠️"
            )
            st.write(
                f"Этот сервис ожидает получить следущее количество документов: {number}."
            )
            st.write(f"Вы попытались отпавить: {len(all_files)}")
            st.write(
                f"Пожалуйста, перепровьте документы и попробуйте повторить отправку."
            )

