# Сайт веломарафонского клуба "Цепная реакция"

### Адрес
https://brevet.omskvelo.ru

### О сайте
Цель работы:
- систематизация разрозненной информации о деятельности веломарафонского движения в г. Омск
- автоматизация организации и документооборота
- мотивация участников на новые подвиги :)

### Стек
Python | Django | Bootstrap | PostgreSQL | Gunicorn | Nginx | Docker

### Запуск
#### Поднять контейнеры
`docker-compose up -d --build`

#### Загрузить дамп
```
docker exec -it brevetomskveloru-web-1 sh
cd /home/brevet/web/brevet
python manage.py loaddata data.json
```

### .gitignore
В исходный код не вошли необходимые для работы файлы:
- .env - файл, содержащий приватные ключи. Вместо него приведён шаблон .env.example.
- static\brevet\img\\* - статические изображения.
