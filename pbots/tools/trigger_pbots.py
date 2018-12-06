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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lilium/")))
import local_settings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <SOURCE_ID|test>".format(sys.argv[0]))
        sys.exit(1)
    source_id = sys.argv[1]
    # Remove the trailing slash, if any
    baseUrl = local_settings.BASE_URL
    if baseUrl[-1] == "/":
        baseUrl = baseUrl[:-1]
    if source_id == "test":
        url = "{}/pbots/api/test/".format(baseUrl)
    else:
        url = "{}/pbots/api/run/{}/".format(baseUrl, source_id)
    r = requests.get(url, auth=HTTPBasicAuth(local_settings.API_USERNAME, local_settings.API_PASSWORD))
    if not r.ok:
        print("HTTP request failed with status code {}".format(r.status_code))
        sys.exit(1)
