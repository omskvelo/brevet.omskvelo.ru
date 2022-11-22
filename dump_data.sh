cd /srv/brevet.omskvelo.ru

docker exec brevetomskveloru_web-blue_1 cd python /home/brevet/web/brevet/manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission -e admin.logentry --indent 2 > dump.json