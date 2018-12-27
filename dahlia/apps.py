# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
dahlia.apps
~~~~~~~~~~~

Configuration for the Dahlia application, a simple
document management system.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.apps import AppConfig


class DahliaConfig(AppConfig):
    """
    Configuration for the Dahlia Django app (a simple document
    management system).
    """
    name = 'dahlia'
