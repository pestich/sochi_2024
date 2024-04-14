import uuid

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

st.title("🔬Классификация текста")


text = st.text_area("Введите текст", height=200)

if "text_data" not in st.session_state or st.session_state.text_data != text:
    st.session_state.text = text
    st.session_state.text_sentiment = None

evaluate_button = st.button("Оценить")


if text and evaluate_button:
    with st.spinner("Обработка..."):
        data = {"content": text}
        response = requests.post("http://backend:8000/api/v1/submission/", json=data)
        result = response.json()

        st.success("Обработка успешно завершена", icon="✅")
        st.text_area(label="Категория докумнента", value=result["content"])

elif evaluate_button and not text:
    st.warning("Введите текст для классификации.", icon="⚠️")

