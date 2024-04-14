import streamlit as st


def main_menu():
    st.sidebar.page_link("app.py", label="Описание")
    st.sidebar.page_link("pages/main.py", label="Основная логика: файлы")
    st.sidebar.page_link("pages/main_archive.py", label="Основная логика: архив")
    st.sidebar.page_link("pages/classifier.py", label="Классификация текста")
    st.sidebar.page_link("pages/classifier_doc.py", label="Классификация документа")
    st.sidebar.page_link("pages/recognize.py", label="Распознование документа")
    st.sidebar.page_link("pages/submission.py", label="Сабмит")
    st.sidebar.page_link("pages/db_request.py", label="Обращение к базе данных")

