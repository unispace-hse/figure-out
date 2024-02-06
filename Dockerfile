FROM python:3.9

ENV PYTHONUNBUFFERED = 1

COPY . /app

WORKDIR /app

RUN pip install -r docker/requirements.txt
