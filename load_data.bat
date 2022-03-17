cd brevet
python manage.py migrate
python manage.py loaddata data.json
python manage.py createcachetable
python manage.py createsuperuser