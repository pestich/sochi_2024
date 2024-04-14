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


st.title("Загрузка архива")

file_types = ["pdf", "docx", "txt", "xlsx", "csv"]

uploaded_archive = st.file_uploader(
    "Загрузите архив в формате zip",
    type=["zip"],
)
add_archive = st.button("Отправить архив")



def safe_remove_directory(path, attempts=3, delay=2):
    """ Пытается безопасно удалить директорию с несколькими попытками и задержкой. """
    for attempt in range(attempts):
        try:
            shutil.rmtree(path)
            print(f"Директория успешно удалена: {path}")
            break
        except PermissionError as e:
            print(f"Не удалось удалить директорию {path}: {e}")
            time.sleep(delay)  # Пауза перед следующей попыткой
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            break
    else:
        print("Не удалось удалить директорию после нескольких попыток.")





if uploaded_archive and add_archive:
    with st.spinner("Обработка..."):
        destination_folder = f"./{st.session_state['session_id']}"
        os.makedirs(destination_folder, exist_ok=True)
        print(uploaded_archive.name)
        temp_file_path = f"temp_{uploaded_archive.name}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_archive, buffer)

        with ZipFile(temp_file_path, "r") as zipf:
            zipf.extractall(destination_folder)

        all_files = []
        file_check = True
        for root, dirs, files in os.walk(destination_folder):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    correct_name = file.encode('cp437').decode('cp866')
                    correct_path = os.path.join(root, correct_name)
                    os.rename(full_path, correct_path)
                    print(f"Извлечён файл: {correct_path}")
                    all_files.append(correct_path)

                except UnicodeDecodeError:
                    print(f"Не удалось скорректировать имя файла: {full_path}")
                    all_files.append(full_path)

                _, file_extension = os.path.splitext(full_path)
                if file_extension[1:] not in file_types:
                    file_check = False
                    st.warning(f"Тип файла {file} не поддерживается.", icon="⚠️")
                    st.warning(
                        f"Файл должен быть в формате: {', '.join(file_types)}", icon="⚠️"
                    )
        try: 
            if len(all_files) == number:
                with contextlib.ExitStack() as stack:
                    files = [("files", (stack.enter_context(open(file_path, "rb")))) for file_path in all_files]

                    data = {"session_id": st.session_state["session_id"]}
                    response = requests.post(
                        "http://backend:8000/api/v1/request/", files=files, data=data
                    )
                    st.write(response.json())
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
        except Exception as ex:
            print(ex)

        finally:
            safe_remove_directory(destination_folder)