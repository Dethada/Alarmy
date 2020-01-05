#!/bin/bash
sudo apt update

# install python stuff
sudo apt install -y python3-dev python3-pip
sudo pip3 install pipenv

# docker stuff
if ! [ -x "$(command -v docker)" ]; then
    curl -fsSL get.docker.com | sh
fi
sudo pip3 install docker-compose

# nodejs and npm
if ! [ -x "$(command -v npm)" ]; then
    curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# required for psycopg2 and flask
sudo apt install -y libpq-dev libatlas-base-dev

# prep .env files
cd agent && cp .env.example .env && cd -
cd frontend && cp .env.example .env && cd -
cd backend && cp .env.example .env && cd -

# we need to prepare the db first
sudo docker-compose up -d --build --remove-orphans postgres

# add postgres to our host record so we dont have to edit the .env to run flask db commands
echo -e '127.0.0.1\tpostgres' | sudo tee -a /etc/hosts

# initialize the database
cd backend
pipenv install
pipenv run flask db upgrade
pipenv run python init_db.py
cd -

# install dependencies for frontend
cd frontend && npm i && cd -

# prepare files required for nginx service
cd frontend
printf 'y' | ./prep.sh
cd -

# build all the services
sudo docker-compose build