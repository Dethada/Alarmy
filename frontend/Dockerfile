FROM nginx:1.17-alpine

RUN rm -f /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Singapore /etc/localtime

COPY config.tar.gz /etc/nginx/
RUN tar -xzf /etc/nginx/config.tar.gz -C /etc/nginx/ --no-same-owner --overwrite
RUN rm -f /etc/nginx/config.tar.gz

RUN mkdir -p /var/www/alarmy.hiding.icu/public
# RUN mkdir /var/www/alarmy.hiding.icu/assets
COPY dist.tar.gz /var/www/alarmy.hiding.icu/public
RUN tar -xzf /var/www/alarmy.hiding.icu/public/dist.tar.gz -C /var/www/alarmy.hiding.icu/public --no-same-owner --overwrite
RUN rm -f /var/www/alarmy.hiding.icu/public/dist.tar.gz
# RUN chown -R nginx:www-data /var/www/alarmy.hiding.icu/public