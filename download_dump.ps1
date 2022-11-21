cd brevet

scp  brevet@brevet.omskvelo.ru:/srv/brevet.omskvelo.ru/dump.json dump.json
rm db.sqlite3
python manage.py migrate
python manage.py loaddata dump.json