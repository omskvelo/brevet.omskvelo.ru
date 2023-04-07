#!/bin/bash

cd /srv/brevet.omskvelo.ru
git pull

docker-compose build web
docker-compose up -d