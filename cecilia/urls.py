# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
cecilia.urls
~~~~~~~~~~~~

URL configuration for the Cecilia app, a dashboard and an API to show
and collect temperature/humidity sensor data.

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.urls import path

from . import views

app_name = "cecilia"
urlpatterns = [
    path("", views.index, name="index"),
    path("sensor_details/<str:sensor_name>/", views.sensor_details, name="sensor_details"),
    path("api/sensor_data/<str:sensor_name>/", views.sensor_data, name="api_sensor_data"),
    path("api/all_sensor_data/", views.all_sensor_data, name="api_all_sensor_data"),
    path("api/blueprint/<str:sensor_name>/", views.blueprint, name="api_blueprint"),
]
