# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
pbots.admin
~~~~~~~~~~~

Django administration interface for the PBOTS app, a dashboard and REST API for
web scraping and mailing list management.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.contrib import admin

from .models import MailingListMember, Source

admin.site.register(MailingListMember)
admin.site.register(Source)
