FROM python:3.11-slim

RUN pip install flask

WORKDIR /app
COPY ./app /app

CMD ["python", "app.py"]

