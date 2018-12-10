# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
cecilia.views
~~~~~~~~~~~~~

Views for the temperature/humidity sensors dashboard and REST
API to acquire data from collectors and to get sensor data.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from typing import Dict

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.templatetags.staticfiles import static

from .models import Sensor, SensorReading


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    Cecilia sensor dashboard.
    :param request: HTTP GET request
    :return: the dashboard for the configured sensors
    """
    sensors = Sensor.objects.all().order_by("id")
    context = {
        "sensors": [{"name": x.name} for x in sensors],
    }
    return render(request, "cecilia/index.html", context)


@login_required
def sensor_details(request: HttpRequest, sensor_name: str) -> HttpResponse:
    """
    Cecilia sensor dashboard.
    :param request: HTTP GET request
    :param sensor_name: name of the sensor (e.g. living_room, attic, basement)
    :return: the dashboard for the configured sensors
    """
    sensor = get_object_or_404(Sensor, name=sensor_name)
    context = {
        "sensor": model_to_dict(sensor, fields=["name", "type", "specs"]),
        "img_url": reverse("cecilia:api_blueprint", kwargs={"sensor_name": sensor_name}),
    }
    return render(request, "cecilia/sensor_details.html", context)


def _get_sensor_data_as_dict(sensor: Sensor, max_results: int) -> Dict:
    """
    Return the sensor data and readings as dict.
    :param sensor: the desired sensor
    :param max_results: maximum number of readings that will be returned
    :return: a dict: name, type, specs, readings (a list of dicts with \
                     temperature, humidity, tstamp)
    """
    # Since Django queries are lazy, the following statement
    # adds a LIMIT clause to the SQL query.
    last_readings = SensorReading.objects.filter(
        sensor=sensor).order_by("-tstamp")[:max_results]
    json_response = model_to_dict(sensor, fields=["name", "type", "specs"])
    json_response["readings"] = []
    for reading in last_readings:
        json_reading = {
            "temperature": reading.temperature,
            "humidity": reading.humidity,
            "tstamp": reading.tstamp.strftime("%Y-%m-%d %H:%M"),
        }
        json_response["readings"].append(json_reading)
    json_response["css_class"] = ""
    json_response["reachable"] = False
    if last_readings:
        last_reading = last_readings[0]
        now = timezone.now()
        last_contact_seconds_ago = (now - last_reading.tstamp).total_seconds()
        # If the sensor has not provided us with data for more than 10 minutes
        # we consider it unreachable.
        if last_contact_seconds_ago <= 600:
            json_response["reachable"] = True
            json_response["css_class"] = last_readings[0].get_css_class()
    return json_response


@csrf_exempt
def sensor_data(request: WSGIRequest, sensor_name: str) -> JsonResponse:
    """
    Return the sensor data if called via GET or save a reading if called via POST.
    :param request: a GET (read sensor data) or POST (save sensor reading) HTTP request
    :param sensor_name: name of the sensor (e.g. living_room, attic, basement)
    :return: if GET, the sensor data as per _get_sensor_data_as_dict, if POST an object with key
    "status" and value "ok"
    """
    sensor = get_object_or_404(Sensor, name=sensor_name)
    # If a reading has been sent via POST, save it to the DB
    # and return some sort of feedback.
    if request.method == "POST":
        temperature = request.POST.get("temperature")
        # The temperature is collected as Celsius * 10
        if temperature:
            temperature = float(temperature) / 10
        humidity = request.POST.get("humidity")
        if humidity:
            humidity = float(humidity)
            SensorReading(tstamp=timezone.now(),
                          temperature=temperature,
                          humidity=humidity,
                          sensor=sensor).save()
        return JsonResponse({"status": "ok"})
    # To GET requests, instead, return only a list of
    # recent readings for the specified sensor.
    max_results = int(request.GET.get("max_results", 1440))
    json_response = _get_sensor_data_as_dict(sensor, max_results)
    return JsonResponse(json_response)


@login_required
def all_sensor_data(request: HttpRequest) -> JsonResponse:
    """
    Return the data of all sensors.
    :param request: HTTP request, usually GET
    :return: a JSON object with the "sensor" key and an array of sensor data as value, each
    item of the array as per _get_sensor_data_as_dict
    """
    sensors = Sensor.objects.all().order_by("id")
    json_response = {"sensors": []}
    for sensor in sensors:
        # Since the sensors roughly perform 1 reading per minute, 1440 maximum results
        # are more or less the readings of the last 24 hours
        json_response["sensors"].append(_get_sensor_data_as_dict(sensor, 1440))
    return JsonResponse(json_response)


@login_required
def blueprint(request: HttpRequest, sensor_name: str) -> HttpResponse:
    """
    Return the floor map image for the specified sensor.
    :param request: a GET (read sensor data) or POST (save sensor reading) HTTP request
    :param sensor_name: name of the sensor (e.g. living_room, attic, basement)
    :return: the floor map for the specified sensor, as PNG image
    """
    image_file_name = settings.CECILIA_BLUEPRINTS.get(sensor_name)
    if not image_file_name:
        return redirect(static("/img/cecilia/blueprint_default.png"))
    with open(image_file_name, "rb") as image_file:
        return HttpResponse(image_file.read(), content_type="image/png")
