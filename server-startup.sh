#! /bin/bash

sudo docker compose stop
sudo docker compose rm -f woodwork
sudo docker image rm -f app-woodwork
sudo docker compose -f docker-compose.yml up --build -d

sudo docker compose exec -T woodwork python manage.py makemigrations works
sudo docker compose exec -T woodwork python manage.py makemigrations
sudo docker compose exec -T woodwork python manage.py migrate
sudo docker compose exec -T woodwork python manage.py collectstatic --noinput
sudo docker compose exec -T woodwork python manage.py cleanup_unused_media --noinput
