# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
dahlia.views
~~~~~~~~~~~~

Views for Dahlia, a simple document management system.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    Dahlia dashboard.
    :param request: HTTP GET request
    :return: an overview of Dahlia's documents
    """
    return render(request, "dahlia/index.html")
