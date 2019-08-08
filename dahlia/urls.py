# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
dahlia.urls
~~~~~~~~~~~

URL configuration for the Dahlia app, a simple
document management system.

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.urls import path

from . import views

# pylint: disable=invalid-name
# Rationale:
#   - app_name and urlpatterns are Django standard names.

app_name = "dahlia"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/category_tree/", views.category_tree, name="api_category_tree"),
]
