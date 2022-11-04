cd /srv/brevet.omskvelo.ru

docker exec -it brevetomskveloru-web-blue-1 sh
cd /home/brevet/web/brevet
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission -e users.profile --indent 2 > dump.json
exit

docker cp brevetomskveloru-web-blue-1:/home/brevet/web/brevet/dump.json .