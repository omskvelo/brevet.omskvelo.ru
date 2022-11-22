#!/bin/bash

cd /srv/brevet.omskvelo.ru
git pull

# Make sure green is running
docker-compose up -d

# Switch to green
docker exec brevetomskveloru_nginx_1 cp /home/brevet/nginx_green.conf /etc/nginx/conf.d/nginx.conf
docker exec brevetomskveloru_nginx_1 nginx -s reload

docker-compose build web-blue
docker-compose up -d

# Switch to blue
docker exec brevetomskveloru_nginx_1 cp /home/brevet/nginx_blue.conf /etc/nginx/conf.d/nginx.conf
docker exec brevetomskveloru_nginx_1 nginx -s reload

docker-compose build web-green
docker-compose up -d

# Kill green
docker stop brevetomskveloru_web-green_1