FROM yummygooey/raspbian-buster:latest

RUN echo 'deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi' > /etc/apt/sources.list

RUN apt update && apt dist-upgrade -y
# FROM python:3.7-alpine

RUN rm -f /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Singapore /etc/localtime

RUN apt install -y python3-dev python3-pip
COPY pip.conf /etc/pip.conf

RUN apt install -y libpq-dev libffi-dev libatlas-base-dev

RUN mkdir /root/backend
RUn pip3 install pipenv
WORKDIR /root/backend

# RUN apk update && \
#     apk add --virtual build-deps gcc musl-dev && \
#     apk add postgresql-dev libffi-dev

# Delete build dependencies
# RUN apk del build-deps

COPY Pipfile Pipfile.lock /root/backend/
RUN pipenv install --skip-lock --verbose

COPY src /root/backend/src
COPY app.py .env /root/backend/

CMD ["pipenv", "run", "python3", "-u", "/root/backend/app.py", "-p", "80"]