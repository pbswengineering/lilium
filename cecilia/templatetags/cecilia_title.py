# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
cecilia.templatetags.cecilia_title
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Custom Django template tag that converts sensor names to pretty human-readable labels.

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def cecilia_title(value: str) -> str:
    """
    Convert a sensor name to a pretty human-readable label
    :param value: name of the sensor (e.g. living_room)
    :return: pretty, human-readable sensor name (e.g. Living Room)
    """
    return value.title().replace("_", " ")
