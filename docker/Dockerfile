FROM python:3.7-alpine

COPY . /api
WORKDIR /api

RUN apk update && \
    apk add --virtual build-deps g++ musl-dev && \
    apk add postgresql-dev && \
    rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt

RUN apk del build-deps gcc musl-dev


EXPOSE 5000
