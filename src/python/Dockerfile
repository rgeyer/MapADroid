FROM python:3.10.2-alpine3.15
ENV PYTHONUNBUFFERED 1
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
                postgresql-dev \
        ;
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install --no-cache-dir -r /code/requirements.txt