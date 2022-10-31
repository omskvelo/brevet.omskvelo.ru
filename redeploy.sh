#!/bin/bash
cd /srv/brevet.omskvelo.ru
git pull

docker-compose up -d

# Switch to green
docker exec brevetomskveloru-nginx-1 cp /home/brevet/nginx_green.conf /etc/nginx/conf.d/nginx.conf
docker exec brevetomskveloru-nginx-1 nginx -s reload

docker-compose build web-blue
docker-compose up -d

# Switch to blue
docker exec brevetomskveloru-nginx-1 cp /home/brevet/nginx_blue.conf /etc/nginx/conf.d/nginx.conf
docker exec brevetomskveloru-nginx-1 nginx -s reload

docker-compose build web-green
docker-compose up -d