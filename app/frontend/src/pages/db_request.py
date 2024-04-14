import uuid

import requests
import streamlit as st
from urllib.parse import unquote

import pandas as pd

from menu import main_menu

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())


st.sidebar.write(f"ID сессии: {st.session_state['session_id']}")

st.sidebar.write("\n")

main_menu()
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("\n")

st.title("🔬Обращение к базе данных")


id = st.text_input('Введите ID сессии')

request_button = st.button("Отправить")


if request_button and id:
    url = 'http://backend:8000/api/v1/db_request/session'
    params = {
        'session_id': id
    }
    headers = {
        'accept': 'application/json'
    }

    response = requests.get(url, params=params, headers=headers)
    st.session_state['initial_dataframe'] = pd.DataFrame(response.json())

if 'initial_dataframe' in st.session_state:
    edited_df = st.data_editor(st.session_state['initial_dataframe'])

    data_button = st.button("Получить данные")
    if data_button:
        filtered_df = edited_df 
        filtered_id = filtered_df.loc[filtered_df['status'] == True, 'id'].reset_index(drop=True)
        if not filtered_id.empty:
            attempt_id = filtered_id[0]
            url = 'http://localhost:8000/api/v1/db_request/files'
            params = {
                'attempt_id': attempt_id
            }
            headers = {
                'accept': 'application/json'
            }

            response = requests.get(url, params=params, headers=headers)
            new_df = pd.DataFrame(response.json())
            st.session_state['new_dataframe'] = new_df
            st.session_state['show_download'] = True


if st.session_state.get('show_download', False):
    st.dataframe(st.session_state.get('new_dataframe', pd.DataFrame()))
    if st.button("Скачать файлы"):
        files_list = st.session_state['new_dataframe']['minio_id'].to_list()
        print(files_list)
        response = requests.post(
                    "http://backend:8000/api/v1/db_request/download/",
                    json=files_list,
                )
                
        if response.status_code == 200:
            # Сохраняем файл на локальном диске
            with open("downloaded_files.zip", "wb") as f:
                f.write(response.content)

            st.download_button(
                label="Скачать ZIP-архив",
                data=response.content,
                file_name="downloaded_files.zip",
                mime="application/zip"
            )
        else:
            st.error("Не удалось загрузить файлы")

