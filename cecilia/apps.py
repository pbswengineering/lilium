# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
cecilia.apps
~~~~~~~~~~~~

Configuration for the Cecilia application, a dashboard and an API to
show and collect temperature/humidity sensor data.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.apps import AppConfig


class CeciliaConfig(AppConfig):
    """
    Configuration for the Cecilia Django app (a dashboard and an API for DHT22
    temperature/humidity sensors).
    """
    name = 'cecilia'
