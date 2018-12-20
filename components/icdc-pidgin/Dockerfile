# To run: docker run -v /path/to/wsgi.py:/var/www/pidgin/wsgi.py --name=pidgin -p 81:80 pidgin
# To check running container: docker exec -it pidgin /bin/bash


FROM quay.io/cdis/python-nginx:1.3.0


ENV appname=pidgin

# number of uwsgi worker processes
ENV UWSGI_CHEAPER 2

RUN apk update \
    && apk add postgresql-libs postgresql-dev libffi-dev libressl-dev \
    && apk add linux-headers musl-dev gcc \
    && apk add curl bash git vim

COPY . /$appname
COPY ./deployment/uwsgi/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY ./deployment/uwsgi/wsgi.py /$appname/wsgi.py
COPY ./deployment/nginx/nginx.conf /etc/nginx/
COPY ./deployment/nginx/uwsgi.conf /etc/nginx/conf.d/nginx.conf
WORKDIR /$appname

RUN python -m pip install --upgrade pip \
    && python -m pip install --upgrade setuptools \
    && pip install -r requirements.txt --src /usr/local/lib/python3.6/site-packages/

RUN mkdir -p /var/www/$appname \
    && mkdir -p /var/www/.cache/Python-Eggs/ \
    && mkdir /run/nginx/ \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log \
    && chown nginx -R /var/www/.cache/Python-Eggs/ \
    && chown nginx /var/www/$appname

EXPOSE 80

RUN COMMIT=`git rev-parse HEAD` && echo "COMMIT=\"${COMMIT}\"" >$appname/version_data.py \
    && VERSION=`git describe --always --tags` && echo "VERSION=\"${VERSION}\"" >>$appname/version_data.py \
    && python setup.py install

WORKDIR /var/www/$appname

CMD /$appname/dockerrun.bash
