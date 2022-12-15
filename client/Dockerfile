FROM node:16.18.0

MAINTAINER Luferov Victor <lyferov@yandex.ru>

ENV HOST 0.0.0.0

RUN apt-get update -y && apt-get upgrade -y
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN yarn

ENV NODE_ENV=production
RUN yarn build

# RUN rm -rf $(ls -A | grep -v .output)

EXPOSE 3000
