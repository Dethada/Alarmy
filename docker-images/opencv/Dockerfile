FROM rpi-base:latest

RUN apt update && apt install -y python3-dev python3-pip

COPY pip.conf /etc/pip.conf

# RUN apt install -y libhdf5-dev libhdf5-serial-dev libhdf5-103 libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 libatlas-base-dev libjasper-dev

RUN apt install -y libpango-1.0-0 libatk1.0-0 libcairo-gobject2 libpangocairo-1.0-0 libqt4-test libtiff5 libqtcore4 libwebp6 libavcodec58 libavutil56 libqtgui4 libavformat58 libgdk-pixbuf2.0-0 libgtk-3-0 libilmbase23 libjasper1 libcairo2 libswscale5 libopenexr23 libhdf5-103 libatlas-base-dev

RUN pip3 install opencv-contrib-python==4.1.0.25