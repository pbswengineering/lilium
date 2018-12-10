#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
collector
~~~~~~~~~

This collector acquires DHT22 readings and sends them to the Lilium server.
The readings can be acquired by three different sources:

   * Arduino Uno with Ethernet shield: collector.py --name=living_room --arduino_ip=192.168.16.11
   * Arduino Uno connected via USB: collector.py --name=attic --usb
   * DHT22 connected to the Raspberry PI via GPIO: collector.py --name=attic --gpio

The following extra Python libraries are required:

   * requests (e.g. python3-requests)
   * serial (e.g. python3-serial, python3-pyserial etc...)
   * Adafruit_Python_DHT (https://github.com/adafruit/Adafruit_Python_DHT)

About the latter, I've found some people mentioning the fact that it's better
to avoid the pip installation; therefore, after downloading the library
archive, it should be installed with `sudo python3 setup.py install`.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

import argparse
from datetime import datetime
import sys
import time
from typing import Dict

import requests
import serial
import Adafruit_DHT

# SERVER_URL = 'https://cecilia-bernacon.rhcloud.com/api/sensor/living_room/'
# SERVER_URL = 'http://www.bernardi.cloud/manager/public/sensor/data'
SERVER_URL = "http://127.0.0.1:8000/cecilia/api/sensor_data/"
LILIUM = True  # As opposed to the PBOTS PHP application
DHT_PIN = '4'
TTY_FILE = '/dev/ttyACM0'


def requests_get(url: str) -> requests.Response:
    """
    Perform an HTTP GET request to the specified URL.
    :param url: target URL of the GET request
    :return: the requests library Response
    """
    while True:
        try:
            return requests.get(url, timeout=120)
        except requests.exceptions.Timeout:
            print("Timeout on GET " + url)
            time.sleep(2)


def requests_post(url: str, data: Dict) -> requests.Response:
    """
    Perform an HTTP POST request to the specified URL.
    :param url: target URL of the POST request
    :param data: dictionary with the data to be POSTed
    :return: the requests library Response
    """
    while True:
        try:
            return requests.post(url, data=data, timeout=120)
        except requests.exceptions.Timeout:
            print("Timeout on POST " + url)
            time.sleep(2)


def parse_temperature_and_humidity(line: str) -> (int, int):
    """
    Parse a DHT22 reading returned from Arduino
    :param line: a CSV-like line in the "temperature;humidity" form
    :return: temperature * 10 in Celsius degrees and humidity percentage
    """
    if not line:
        return None, None
    v = line.strip().split(";")
    temperature = int(round(float(v[0])))
    humidity = int(round(float(v[1])))
    return temperature, humidity


def post_reading_to_server(sensor_name: str, temperature: int, humidity: int) -> None:
    """
    Send a DHT22 reading to the Lilium server.
    :param sensor_name: name of the sensor (e.g. living_room, basement, attic)
    :param temperature: temperature * 10, in Celsius degrees
    :param humidity: 0-100 humidity percentage
    :return: None
    """
    if temperature is None and humidity is None:
        return
    if not temperature:
        temperature = 0
    if not humidity:
        humidity = 0
    now = datetime.now()
    reading = {
        "temperature": temperature,
        "humidity": humidity
    }
    server_url = SERVER_URL
    if LILIUM:
        # Lilium wants the server_name as part of the URL (a bit more RESTy)
        # I am not sure what would be the point of using urllib.parse.urljoin, see
        # https://stackoverflow.com/questions/1793261/how-to-join-components-of-a-path-when-you-are-constructing-a-url-in-python
        if server_url[-1] != "/":
            server_url += "/"
        server_url += sensor_name + "/"
    else:
        # PBOTS PHP read the sensorName key of the dict
        reading["sensorName"] = sensor_name
        # PBOTS PHP read the timestamp from the collector
        reading["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")
    req = requests_post(server_url, data=reading)
    print(now, req.text.strip())


def collect_from_usb(sensor_name: str) -> None:
    """
    Collect a DHT22 temperature and humidity reading from an Arduino Uno via USB.
    :param sensor_name: name of the sensor (e.g. living_room, basement, attic)
    :return: None
    """
    ser = serial.Serial(TTY_FILE, 9600)
    line = ser.readline().decode("utf-8")
    temperature, humidity = parse_temperature_and_humidity(line)
    post_reading_to_server(sensor_name, temperature, humidity)


def collect_from_gpio(sensor_name: str) -> None:
    """
    Collect a DHT22 temperature and humidity reading from a DHT22 connected to
    the Raspberry PI via GPIO.
    :param sensor_name: name of the sensor (e.g. living_room, basement, attic)
    :return: None
    """
    # TODO: Verify the time required for the collection.
    # TODO: It should be around a minute, not less...
    humidity, temperature, count = 0, 0, 0
    for i in range(20):
        h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT_PIN)
        temperature += t * 10
        humidity += h
        count += 1
        time.sleep(2.75)
    temperature /= count
    humidity /= count
    temperature = int(round(temperature))
    humidity = int(round(humidity))
    post_reading_to_server(sensor_name, temperature, humidity)


def collect_from_test(sensor_name: str) -> None:
    """
    Send to the server fake data, to test the REST PI
    :param sensor_name: name of the sensor (e.g. living_room, basement, attic)
    :return: None
    """
    temperature, humidity = 194, 61
    post_reading_to_server(sensor_name, temperature, humidity)


def collect_from_arduino(sensor_name: str, arduino_ip: str) -> None:
    """
    Collect a DHT22 temperature and humidity reading from an Arduino Uno
    connected to the Ethernet network.
    :param sensor_name: name of the sensor (e.g. living_room, basement, attic)
    :param arduino_ip: IP address of the Arduino Uno (e.g. 192.168.16.11)
    :return: None
    """
    arduino_req = requests_get("http://{}".format(arduino_ip))
    temperature, humidity = parse_temperature_and_humidity(arduino_req.text)
    post_reading_to_server(sensor_name, temperature, humidity)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Collect data from DHT22 sensors.
The data can be acquired both from Arduino Uno with network interfaces and from Raspberry PI via GPIO.
    """)
    parser.add_argument("name",
                        type=str,
                        help="Name of the sensor (living_room, attic or basement)")
    parser.add_argument("--arduino",
                        metavar="ARDUINO_IP",
                        type=str,
                        help="Collect a reading from the Arduino with this IP address (e.g. 192.168.16.11)")
    parser.add_argument("--gpio",
                        action="store_true",
                        help="Collect a reading from the GPIO interface of the Raspberry PI")
    parser.add_argument("--usb",
                        action="store_true",
                        help="Collect a reading from an Arduino Uno connected via USB")
    parser.add_argument("--test",
                        action="store_true",
                        help="Send fake data to the server, without collecting it from any physical sensor")
    args = parser.parse_args()
    # There is an implicit cast form bool to int (0/1) and an explicity (possible) cast from NoneType to bool
    selected_modes_count = bool(args.arduino) + bool(args.gpio) + bool(args.usb) + bool(args.test)
    if selected_modes_count == 0:
        sys.stderr.write(
            "ERROR: You must select a collection mode (--arduino=ARDUINO_IP, --gpio or --usb)")
        parser.print_help(sys.stderr)
        sys.exit(1)
    elif selected_modes_count > 1:
        sys.stderr.write(
            "ERROR: You must select only one collection mode (--arduino=ARDUINO_IP, --gpio or --usb)")
        parser.print_help(sys.stderr)
        sys.exit(1)
    elif args.arduino:
        collect_from_arduino(args.name, args.arduino)
    elif args.gpio:
        collect_from_gpio(args.name)
    elif args.usb:
        collect_from_usb(args.name)
    else:
        collect_from_test(args.name)
