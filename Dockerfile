FROM python:3.10-alpine3.14

COPY dht.py /

SHELL ["/bin/sh", "-euxo", "pipefail", "-c"]

RUN apk add --no-cache libgpiod \
    && apk add --no-cache --virtual build gcc libc-dev \
    && pip3 install --no-cache-dir adafruit-circuitpython-dht RPi.GPIO==0.7.1a4 \
    && apk del --no-network --purge build \
    && chmod +x /dht.py

CMD ["python", "./dht.py -g 22 -i 5"]
