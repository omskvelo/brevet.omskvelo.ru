cd /srv/brevet.omskvelo.ru

docker exec -it brevetomskveloru_web-blue_1 sh
cd /home/brevet/web/brevet
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission -e users.profile -e admin.logentry --indent 2 > dump.json
exit

docker cp brevetomskveloru_web-blue_1:/home/brevet/web/brevet/dump.json .