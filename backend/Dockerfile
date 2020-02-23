FROM python:3.7-buster

RUN apt install -y libpq-dev libffi-dev libatlas-base-dev

RUN mkdir /root/backend
WORKDIR /root/backend

COPY requirements.txt /root/backend/
RUN pip install -r /root/backend/requirements.txt

COPY src /root/backend/src
COPY app.py .env /root/backend/

CMD ["python3", "-u", "/root/backend/app.py", "-p", "5000"]