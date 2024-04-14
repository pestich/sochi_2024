FROM python:3.11

WORKDIR /app

EXPOSE 8501

COPY ./requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY ./src/ /app

ENTRYPOINT ["streamlit", "run", "app.py"]