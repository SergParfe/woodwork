#! /bin/bash

docker-compose stop
docker-compose rm -f woodwork
docker image rm -f woodwork-woodwork
docker-compose -f docker-compose.yml up --build -d
docker-compose exec -T woodwork python manage.py makemigrations works
docker-compose exec -T woodwork python manage.py migrate
