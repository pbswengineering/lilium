# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
cecilia.models
~~~~~~~~~~~~~~

Models to manage the available temperature/humidity sensors and
to store their readings.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.db import models


class Sensor(models.Model):
    """
    Generic temperature and humidity sensor.
    """
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    specs = models.CharField(max_length=256)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the Sensor
        :return: the sensor name
        """
        return self.name


class SensorReading(models.Model):
    """
    Timestamped reading from a temperature and humidity sensor.
    """
    tstamp = models.DateTimeField()
    temperature = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the reading
        :return: a text describing temperature and humidity
        """
        return "{}: temp {}°, hum {}%".format(self.tstamp, self.temperature, self.humidity)

    def get_css_class(self):
        """
        Return a CSS class to be applied to a Boostrap 4 card that shows
        at glance the climate determined by the reading's temperature
        and humidity (red -> hot, yellow -> somewhat hot,
        green -> comfortable, blue -> too cold, no class -> no data)
        :return: card-red, card-yellow, card-green, card-blue or an empty string
        """
        if self.temperature is None or self.humidity is None:
            return ""
        if self.temperature >= 25 or self.humidity <= 20 or self.humidity >= 80:
            return "card-red"
        if self.temperature >= 23:
            return "card-yellow"
        if self.temperature >= 19:
            return "card-green"
        return "card-blue"
