# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
matrimonio-comune-montecastrilli
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scraper for the wedding register of the "Comune di Montecastrilli".

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

import json
import re
import requests
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag


SOURCE = "Matrimoni del Comune di Montecastrilli"
# Historical archive, it doesn't contain the most recent weddings but it's good for testing
# SUMMARY_URL = "http://halleyweb.com/c055017/mc/mc_matri_gridev_messi_datigrid.php?sto=1&x=1"
# Most recent weddings, good for live usage
SUMMARY_URL = "http://halleyweb.com/c055017/mc/mc_matri_gridev_messi_datigrid.php?x=1"
JS_DETAIL_PATTERN = re.compile(r"visualizza_dettaglio\((\d*?)\s*,\s*(\d*),\s*(\d*)\)")
DETAIL_URL_TEMPLATE = "http://halleyweb.com/c055017/mc/mc_matri_gridev_dettaglio.php?x=1&id_pubbl={}&interno={}"
JS_DOCUMENT_PATTERN = re.compile("window.open\\('(.*?)'\\)")
DOCUMENT_URL_TEMPLATE = "http://halleyweb.com/c055017/mc/{}"


def date_ita_to_iso(ita: str) -> Optional[str]:
    """
    Convert an Italian date to the ISO format
    :param ita: date in Italian format (e.g. 31/12/2018 or 31-12-2018)
    :return: the date in ISO format (e.g. 2018-12-31)
    """
    if len(ita) != 10:
        return None
    year = int(ita[6:])
    month = int(ita[3:5])
    day = int(ita[:2])
    return "{:04d}-{:02d}-{:02d}".format(year, month, day)


def parse_detail(url_detail: str) -> Dict[str, str]:
    """
    Parse the detail page of a publication.
    :param url_detail: URL of the publication's detail page
    :return: a dict with the publication details
    """
    detail_page = requests.get(url_detail, allow_redirects=True)
    soup = BeautifulSoup(detail_page.content, 'html.parser')
    trs = soup.find_all("tr")
    pub = {
        "url": url_detail,
        "source": SOURCE,
        "attachments": [],
    }
    for tr in trs:
        tds = tr.find_all("td")
        key = tds[0].get_text().strip().replace("\u00A0", "").upper()
        value = tds[1].get_text().strip().replace("\u00A0", "")
        if key.find("NUMERO PUBBLICAZIONE") != -1:
            pub["number"] = value
        elif key.find("MITTENTE") != -1:
            pub["publisher"] = value
        elif key.find("TIPO ATTO") != -1:
            pub["type"] = value
        elif key.find("OGGETTO ATTO") != -1:
            pub["subject"] = value
        elif key.find("DATA INIZIO PUBBLICAZIONE") != -1:
            pub["date_start"] = date_ita_to_iso(value)
        elif key.find("DATA FINE PUBBLICAZIONE") != -1:
            pub["date_end"] = date_ita_to_iso(value)
        elif key.find("DOCUMENT") != -1:
            a_tags = tds[1].find_all("a")
            for a in a_tags:
                match = JS_DOCUMENT_PATTERN.search(a["onclick"])
                if match:
                    pub["attachments"].append({
                        "name": a.get_text(),
                        "url": DOCUMENT_URL_TEMPLATE.format(match.group(1))
                    })
    return pub


def parse_row(row: Tag) -> Optional[Dict[str, str]]:
    """
    Parse a row of the table of publications.
    :param row: a row of the table of publications
    :return: a dict with the publication details or None if the parsing failed
    """
    js_detail_match = JS_DETAIL_PATTERN.search(row.get_text())
    if js_detail_match:
        pub_id = js_detail_match.group(1)
        internal = js_detail_match.group(2)
        url_detail = DETAIL_URL_TEMPLATE.format(pub_id, internal)
        return parse_detail(url_detail)
    return None


def scrape() -> List[Dict[str, str]]:
    """
    Scrape the register.
    :return: a list of dictionaries of the current publications
    """
    summary_page = requests.get(SUMMARY_URL, allow_redirects=True)
    soup = BeautifulSoup(summary_page.content, 'html.parser')
    rows = soup.find_all("row")
    pubs = []
    for row in rows:
        pub = parse_row(row)
        if pub:
            pubs.append(pub)
    return pubs


if __name__ == "__main__":
    print(json.dumps(scrape()))
