# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
pbots.urls
~~~~~~~~~~

URLs configuration for the PBOTS app, a dashboard and REST API for
web scraping and mailing list management.

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.urls import path

from . import views

# pylint: disable=invalid-name
# Rationale:
#   - app_name and urlpatterns are Django standard names.

app_name = "pbots"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/status/", views.status, name="api_status"),
    path("api/run/<int:source_id>/", views.run, name="api_run"),
    path("api/stop/<int:source_id>/", views.stop, name="api_stop"),
    path("api/test/", views.test, name="api_test"),
]
