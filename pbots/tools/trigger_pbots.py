#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
trigger_pbots
~~~~~~~~~~~~~

Script to send an HTTP GET request to the Lilium pbots/run endpoint.
Apparently cURL on CeciliaNAS doesn't work very well, so I wrote
this simple script.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

import os
import sys

import requests
from requests.auth import HTTPBasicAuth

# pylint: disable=import-error,wrong-import-position
# Rationale:
#   - This is an hack, local_settings are in a known FS position.
#   - The import cannot be imported before os and sys.
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lilium/")))
import local_settings


def trigger_pbots(source_id: str) -> None:
    """
    Ajax call to start a PBOTS scraper.
    :param source_id: ID of the scraper to start
    """
    # Remove the trailing slash, if any
    base_url = local_settings.BASE_URL
    if base_url[-1] == "/":
        base_url = base_url[:-1]
    if source_id == "test":
        url = "{}/pbots/api/test/".format(base_url)
    else:
        url = "{}/pbots/api/run/{}/".format(base_url, source_id)
    return requests.get(url, auth=HTTPBasicAuth(local_settings.API_USERNAME,
                                                local_settings.API_PASSWORD))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <SOURCE_ID|test>".format(sys.argv[0]))
        sys.exit(1)
    SOURCE_ID = sys.argv[1]
    REQUEST = trigger_pbots(SOURCE_ID)
    if not REQUEST.ok:
        print("HTTP request failed with status code {}".format(REQUEST.status_code))
        sys.exit(1)
