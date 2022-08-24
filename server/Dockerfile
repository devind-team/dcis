FROM python:3.10.5-slim

MAINTAINER Luferov Victor <lyferov@yandex.ru>

ENV PYTHONUNBUFFERED 1
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN apt-get update -y && \
    pip install poetry && \
    pip install --upgrade pip && \
    apt-get install build-essential -y && \
    apt-get install libreoffice -y  && \
    apt-get install libreoffice --upgrade

# Copy application
COPY . /usr/src/app
RUN poetry install --no-dev

# Enter point
CMD ['poetry']
