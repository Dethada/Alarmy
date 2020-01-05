FROM yummygooey/raspbian-buster:latest

RUN echo 'deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi' > /etc/apt/sources.list

RUN apt update && apt dist-upgrade -y

RUN apt install -y python3-dev python3-pip

RUN apt install -y libpq-dev libpango-1.0-0 libatk1.0-0 libcairo-gobject2 libpangocairo-1.0-0 libqt4-test libtiff5 libqtcore4 libwebp6 libavcodec58 libavutil56 libqtgui4 libavformat58 libgdk-pixbuf2.0-0 libgtk-3-0 libilmbase23 libjasper1 libcairo2 libswscale5 libopenexr23 libhdf5-103 libatlas-base-dev libhdf5-dev libhdf5-serial-dev

COPY pip.conf /etc/pip.conf
RUN mkdir /root/agent
RUN pip3 install pipenv
WORKDIR /root/agent

COPY Pipfile Pipfile.lock tensorflow-2.0.0-cp37-none-linux_armv7l.whl /root/agent/
RUN pipenv install --skip-lock

RUN rm -f /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Singapore /etc/localtime

COPY agent /root/agent/agent
COPY ssd_mobilenet /root/agent/ssd_mobilenet
COPY .env /root/agent/.env

CMD ["pipenv", "run", "python3", "-u", "/root/agent/agent/main.py"]