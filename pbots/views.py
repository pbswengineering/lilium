# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
pbots.views
~~~~~~~~~~~

Views for the PBOTS dashboard and REST API for
web scraping and mailing list management.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from lilium.django_basic_auth import logged_in_or_basicauth

from .commands import run_command, send_email
from .models import Source


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    PBOTS dashboard, showing the Source scrapers status at glance.
    :param request: HTTP GET request
    :return: the dashboard for the configured PBOTS
    """
    sources = Source.objects.order_by("name")
    now = timezone.now()
    # Add some colour to the PBOTS table row
    for source in sources:
        if source.executions > 0:
            if not source.last_execution_ok:
                source.css_class = "table-danger"
            elif (now - source.started_at).days >= 7:
                source.css_class = "table-warning"
            else:
                source.css_class = "table-success"
    context = {
        "sources": sources
    }
    return render(request, "pbots/index.html", context)


@login_required
def status(request: HttpRequest) -> JsonResponse:
    """
    Return the Source scrapers status, including CSS classes to show it visually.
    :param request: an HTTP request
    :return: a dict with a sources keys, containing the Source model properties plus "css_class"
    """
    sources = Source.objects.order_by("name")
    sources = [model_to_dict(s) for s in sources]
    now = timezone.now()
    # Add some colour to the PBOTS table row
    for source in sources:
        if source["executions"] > 0:
            if not source["last_execution_ok"]:
                source["css_class"] = "table-danger"
            elif not source["finished_at"]:
                if (now - source["started_at"]).days >= 7:
                    source["css_class"] = "table-warning"
                else:
                    source["css_class"] = "table-primary"
            else:
                source["css_class"] = "table-success"
        if source["started_at"]:
            source["started_at"] = source["started_at"].strftime(
                "%Y-%m-%d %H:%M:%S")
        if source["finished_at"]:
            source["finished_at"] = source["finished_at"].strftime(
                "%Y-%m-%d %H:%M:%S")
    return JsonResponse({
        "sources": sources
    })


@csrf_exempt
@logged_in_or_basicauth()
def run(request: HttpRequest, source_id: int) -> JsonResponse:
    """
    Run a Source scraper
    :param request: an HTTP request
    :param source_id the Source ID of the PBOTS to run
    :return: a dict with a "message" key (the operation result)
    """
    source = get_object_or_404(Source, pk=source_id)
    if source.running:
        message = "Source {} is already running".format(source_id)
    else:
        source.mark_start()
        run_command(source)
        message = "Source {} started".format(source_id)
    return JsonResponse({
        "message": message
    })


@login_required
def stop(request: HttpRequest, source_id: int) -> JsonResponse:
    """
    Mark the spceified Source scraper as stopped (ACHTUNG! The related \
    background processes may still be running).
    :param request: an HTTP request
    :param source_id the Source ID of the PBOTS to stop
    :return: a dict with a "message" key (the operation result)
    """
    source = get_object_or_404(Source, pk=source_id)
    if not source.running:
        message = "Source {} is not running".format(source_id)
    else:
        source.mark_stop()
        message = "Source {} stopped".format(source_id)
    return JsonResponse({
        "message": message
    })


@csrf_exempt
@logged_in_or_basicauth()
def test(request: HttpRequest) -> JsonResponse:
    """
    Send a newsletter test email to the current user's email address.
    :param request: an HTTP request
    :return: a dict with a "message" key (the operation result)
    """
    publications = [{
        "id": 421,
        # pylint: disable=line-too-long
        # Rationale:
        #   - I prefer to keep this URL on a single line. Perhaps I could move it
        #     to a constant of some sort, but it would go against the spirit of
        #     this simple test.
        "url": "http://halleyweb.com/c11111/mc/mc_matri_gridev_dettaglio.php?x=1&id_pubbl=11111&interno=0",
        "number": "948",
        "publisher": "Ufficio Stato Civile",
        "pub_type": "Pubblicazione di matrimonio",
        "subject": "Pubblicazione di matrimonio di Rossi Mario e Verdi Maria",
        "date_start": "2018-12-04",
        "date_end": "2018-12-12",
        "source_id": 7,
        "attachments": [{
            "id": 792,
            "name": "Pubblicazione_di_matrimonio.PDF.p7m",
            "url": "http://halleyweb.com/c111111/mc/mc_attachment.php?x=1&mc=1111"
        }]
    }]
    recipients = [request.user.email]
    send_email(recipients, "Test", publications)
    return JsonResponse({
        "message": "A test email has been sent to {}".format(request.user.email)
    })
