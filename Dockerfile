#FROM alpine/git:v2.32.0 AS git

#RUN mkdir /app
#WORKDIR /app

#CMD [ "clone", "https://github.com/adafruit/Adafruit_CircuitPython_DHT.git" ]

FROM python:3.10-alpine3.14

COPY dht.py /

RUN apk add --no-cache libgpiod py3-rpigpio \
    ; \
    pip3 install --no-cache-dir adafruit-circuitpython-dht; \
#    pip3 install --no-cache-dir rpi.gpio; \
#    apk del --no-network --purge .build; \
    chmod +x /dht.py

#COPY --from=git /app /app
#RUN pip install -r requirements.txt

#CMD ["python", "./dht.py"]
CMD ["sleep", "4800"]