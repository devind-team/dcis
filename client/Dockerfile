FROM node:16.13.2

MAINTAINER Luferov Victor <lyferov@yandex.ru>

ENV HOST 0.0.0.0

RUN apt-get update -y && apt-get upgrade -y
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package.json /usr/src/app
RUN yarn

COPY . /usr/src/app
# COPY .env.production .env

ENV NODE_ENV=production
RUN yarn build

EXPOSE 3000
