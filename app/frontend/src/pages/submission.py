import time
import uuid

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

st.title("🔬Сабмит для хакатона")

st.write("\n")
st.write("Загрузите файл в формате csv.")
st.write("Файл должен содержать два столбца. Второй столбец должен быть текстовый.")

uploaded_file = st.file_uploader(
    "",
    type=["csv"],
)
add_data = st.button("Отправить")


if uploaded_file and add_data:

    df = pd.read_csv(uploaded_file)
    if df.shape[1] == 2 and df.iloc[:, 1].dtypes == "object":
        progress_text = "Документ обрабатывается. Пожалуйста, подождите..."
        my_bar = st.progress(0, text=progress_text)
        percent_complete = 0
        lenght = len(df.iloc[:, 1])
        step = round(1 / lenght, 4)

        results = []
        for idx in range(lenght):
            data = {"content": df.iloc[:, 1][idx]}
            response = requests.post(
                "http://backend:8000/api/v1/submission/", json=data
            )
            result = response.json()
            results.append(result["content"])

            percent_complete += step
            if percent_complete < 1:
                my_bar.progress(percent_complete, text=progress_text)
        time.sleep(0.5)
        my_bar.empty()
        st.success("Обработка успешно завершена", icon="✅")
        df["predict"] = results
        st.dataframe(df)
    else:
        st.warning("Загруженный файл не соответствует требованиям.", icon="⚠️")

elif add_data and not uploaded_file:
    st.warning("Загрузите документ для классификации.", icon="⚠️")
