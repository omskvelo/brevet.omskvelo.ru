cd brevet

scp  -o KexAlgorithms=diffie-hellman-group1-sha1 -P 11022 brevet@omskvelo.ru:/srv/brevet.omskvelo.ru/dump.json dump.json
rm db.sqlite3
python manage.py migrate
python manage.py loaddata dump.json