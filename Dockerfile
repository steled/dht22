FROM python:3.12.3-alpine3.19

COPY dht.py /

SHELL ["/bin/sh", "-euxo", "pipefail", "-c"]

RUN apk add --no-cache libgpiod \
    && apk add --no-cache --virtual build gcc libc-dev  \
    && pip3 install --no-cache-dir prometheus_client ConfigArgParse adafruit-circuitpython-dht RPi.GPIO==0.7.1a4 \
    && apk del --no-network --purge build \
    && chmod +x /dht.py

ENTRYPOINT ["python", "./dht.py"]
