#FROM alpine/git:v2.32.0 AS git

#RUN mkdir /app
#WORKDIR /app

#CMD [ "clone", "https://github.com/adafruit/Adafruit_CircuitPython_DHT.git" ]

FROM python:3.10-alpine3.14

COPY dht.py /

RUN apk add --no-cache \
    apk add git libgpiod2 \
    && rm -rf /var/cache/apk/* \
    ; \
    pip3 install adafruit-circuitpython-dht; \
    chmod +x /dht.py

#COPY --from=git /app /app
#RUN pip install -r requirements.txt

CMD ["python", "./dht.py"]