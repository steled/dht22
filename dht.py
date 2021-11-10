#!/usr/bin/env python3

# Prometheus exporter for DHT22 running on raspberrypi
# Source: https://github.com/clintjedwards/dht22_exporter/blob/master/dht22_exporter.py
# Usage: ./dht -g <gpio_pin_number> -i <poll_time_in_seconds> [-a <exposed_address> -p <exposed_port>]
# Ex: ./dht -g 4 -i 2

import time
import board
import argparse

from prometheus_client import Gauge, start_http_server

import adafruit_dht

# Create a metric to track time spent and requests made.
dht22_temperature_celsius = Gauge(
    'dht22_temperature_celsius', 'Temperature in celsius provided by dht sensor')
dht22_temperature_fahrenheit = Gauge(
    'dht22_temperature_fahrenheit', 'Temperature in fahrenheit provided by dht sensor')
dht22_humidity = Gauge(
    'dht22_humidity', 'Humidity in percents provided by dht sensor')

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gpio", dest="gpio", type=str,
                        required=True, help="GPIO pin number on which the sensor is plugged in")
    parser.add_argument("-a", "--address", dest="addr", type=str, default=None,
                        required=False, help="Address that will be exposed")
    parser.add_argument("-i", "--interval", dest="interval", type=int,
                        required=True, help="Interval sampling time, in seconds")
    parser.add_argument("-p", "--port", dest="port", type=int, default=9100,
                        required=False, help="Port that will be exposed")
    return parser

def init_dhtdevice(pin) -> adafruit_dht.DHT22:
    # GPIO <https://www.raspberrypi.org/documentation/usage/gpio/>
    # dictionary idea <https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/57>
    boardspins = {'D0': board.D0, 
    'D1': board.D1, 'D2': board.D2, 'D3': board.D3, 'D4': board.D4, 'D5': board.D5, 
    'D6': board.D6, 'D7': board.D7, 'D8': board.D8, 'D9': board.D9, 'D10': board.D10, 
    'D11': board.D11, 'D12': board.D12, 'D13': board.D13, 'D14': board.D14, 'D15': board.D15, 
    'D16': board.D16, 'D17': board.D17, 'D18': board.D18, 'D19': board.D19, 'D20': board.D20, 
    'D21': board.D21, 'D22': board.D22, 'D23': board.D23, 'D24': board.D24, 'D25': board.D25, 
    'D26': board.D26, 'D27': board.D27}

    pin = boardspins[str(pin)]

    # Initial the dht device, with data pin connected to:
    dhtDevice = adafruit_dht.DHT22(pin)

    return dhtDevice

def read_sensor(dhtDevice):
    humidity = dhtDevice.humidity
    temperature = dhtDevice.temperature

    if humidity is None or temperature is None:
        return

    if humidity > 200 or temperature > 200:
        return

    dht22_humidity.set('{0:0.1f}'.format(humidity))
    dht22_temperature_fahrenheit.set(
        '{0:0.1f}'.format(9.0/5.0 * temperature + 32))
    dht22_temperature_celsius.set(
        '{0:0.1f}'.format(temperature))

def main():
    parser = init_argparse()
    args = parser.parse_args()

    dhtDevice = init_dhtdevice(pin=args.gpio)

    if args.addr is not None:
        start_http_server(args.port, args.addr)
    else:
        start_http_server(args.port)

    while True:
        try:
            read_sensor(dhtDevice)
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(args.interval)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

    time.sleep(args.interval)

main()
