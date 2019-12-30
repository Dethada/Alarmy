#!/bin/bash
SERVICE=$1
sudo docker-compose stop $SERVICE # this will stop only the selected container
sudo docker-compose rm -f $SERVICE # this will remove the docker container permanently 
sudo docker-compose up -d --build --remove-orphans $SERVICE
