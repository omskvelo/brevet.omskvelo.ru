#!/bin/bash
cd /srv/brevet.omskvelo.ru
git pull

docker-compose up -d --build