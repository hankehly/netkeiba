FROM python:3.6.7

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
