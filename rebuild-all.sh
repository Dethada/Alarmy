#!/bin/bash
# Gateway
cd frontend
./prep.sh
cd -

sudo docker-compose down
sudo docker-compose up -d --build