#! /bin/bash

docker-compose stop
docker-compose rm -f woodwork
docker image rm -f woodwork-woodwork
docker image prune -af
docker-compose -f docker-compose.yml up --build -d
