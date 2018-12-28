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
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Category


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    Dahlia dashboard.
    :param request: HTTP GET request
    :return: an overview of Dahlia's documents
    """
    return render(request, "dahlia/index.html")


@login_required
def category_tree(request: HttpRequest) -> JsonResponse:
    """
    Return the category tree, in the JSTree "id/parent" format.
    :param request: HTTP request, usually GET
    :return: a JSON object with the category tree
    """
    categories = Category.objects.all().order_by("id")
    json_response = {"categories": []}
    for category in categories:
        json_response["categories"].append({
            "id": category.id,
            "parent": category.parent_id or "#",
            "text": category.name,
        })
    return JsonResponse(json_response)
