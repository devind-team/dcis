FROM node:16.14.2

MAINTAINER Luferov Victor <lyferov@yandex.ru>

ENV HOST 0.0.0.0

RUN apt-get update -y && apt-get upgrade -y
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN yarn

ENV NODE_ENV=production
RUN yarn build

EXPOSE 3000
