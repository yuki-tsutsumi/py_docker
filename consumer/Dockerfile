FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
# コンテナ内で必要なパッケージをインストール
RUN apk add --no-cache build-base \
 && pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
 && apk del build-base

COPY consumer.py .
