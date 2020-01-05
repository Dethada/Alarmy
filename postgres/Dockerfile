FROM postgres:12-alpine

RUN rm -f /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Singapore /etc/localtime

COPY init.sql /docker-entrypoint-initdb.d/
