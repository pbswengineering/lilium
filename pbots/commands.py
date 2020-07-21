# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
pbots.commands
~~~~~~~~~~~~~~

Commands that implement the scraping and mailing logic for each PBOTS
data source.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from email.mime.image import MIMEImage
import json
from logging import getLogger, Logger
import os
import re
import subprocess
import sys
import threading
import traceback
from typing import Callable, Dict, List, Optional, Union

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import loader

from .models import MailingListMember, Publication, PublicationAttachment, Source


def _wrap_command(source: Source,
                  logger: Logger,
                  func: Callable[[Source, Logger], None]) -> None:
    """
    Run a function that implements a PBOTS command making sure that errors are
    handled and that execution start/stop and timing are tracked in the DB.
    IMPORTANT: the command is executed in the current thread (see run_command
    for executing it on a separate thread).
    :param source: scraping data source
    :param logger: source-specific logger
    :param func: function that implements the command (it must take the \
                 source and the logger as arguments)
    """
    try:
        func(source, logger)
        source.last_execution_ok = True
        logger.info("{}: executed correctly.".format(source.command))
    # pylint: disable=broad-except
    # Rationale:
    #   - A scraping function can be implemented in many ways and I want
    #     to make sure that most of execution errors are tracked.
    except Exception:
        logger.error("{}: interrupted with errors.".format(source.command))
        logger.error(traceback.format_exc())
        source.last_execution_ok = False
    source.mark_stop()  # implicit "source.save()"


def run_command(source: Source) -> None:
    """
    Run a PBOTS command (usually a function that scrapes and mails) on
    a separate thread.
    :param source: scraping data source
    """
    logger = getLogger("commands.{}".format(source.command))
    logger.info("run_command: %s", source.command)
    try:
        this_module = sys.modules[__name__]
        func = getattr(this_module, source.command)
        thread = threading.Thread(target=_wrap_command, args=(
            source, logger, func), kwargs={})
        thread.setDaemon(True)
        thread.start()
        logger.info("Thread started")
    # pylint: disable=broad-except
    # Rationale:
    #   - I want to make sure to track most of problems that could
    #     arise when starting scraping threads.
    except Exception:
        logger.error("Could not start the thread due to an exception.")
        logger.error(traceback.format_exc())
        source.last_execution_ok = False
        source.mark_stop()


def _add_publications(source: Source,
                      logger: Logger,
                      json_as_text: str) -> None:
    """
    Add the publications found by a scraper to the DB.
    :param source: scraping data source
    :param logger: source-specific logger
    :param json_as_text: the JSON (as string) returned by the scraper
    """
    structured = json.loads(json_as_text)
    if not structured:
        logger.info("There are no new publications.")
        return
    for json_pub in structured:
        subject = json_pub.get("subject")
        found = Publication.objects.filter(subject=subject, source=source)
        if not subject or found:
            continue
        logger.debug("Adding new publication: {}".format(subject))
        pub = Publication()
        pub.url = json_pub.get("url")
        pub.number = json_pub.get("number")
        pub.publisher = json_pub.get("publisher")
        pub.pub_type = json_pub.get("type")
        pub.subject = json_pub.get("subject")
        pub.date_start = json_pub.get("date_start")
        pub.date_end = json_pub.get("date_end")
        pub.source = source
        pub.save()
        if "attachments" in json_pub:
            for json_pub_att in json_pub["attachments"]:
                att = PublicationAttachment()
                att.name = json_pub_att.get("name")
                att.url = json_pub_att.get("url")
                att.publication = pub
                att.save()


def send_email(recipients: List[str],
               title: str,
               publications: Union[List[Publication], List[Dict]]) -> None:
    """
    Send a newsletter to the specified recipients.
    ACHTUNG! Do not call it directly but for test purposes.
    The PBOTS commands should use _run_mailing_list, instead.
    :param recipients: email recipients
    :param title: title of the newsletter
    :param publications: list of publications to be sent
    """
    context = {
        "title": title,
        "publications": publications,
    }
    subject = "Newsletter {}".format(title)
    template_plaintext = loader.get_template("mailing_list/publications.txt")
    email = EmailMultiAlternatives(
        subject,
        template_plaintext.render(context),
        settings.EMAIL_FROM,
        [settings.EMAIL_FROM],
        bcc=recipients,
        reply_to=settings.EMAIL_REPLY_TO
    )
    # This is required for images to be displayed within the message body
    email.mixed_subtype = 'related'
    template_html = loader.get_template("mailing_list/publications.html")
    email.attach_alternative(template_html.render(context), "text/html")
    # The logo will be added as MIME image attachment and referenced in the
    # img src via cid:xxxx because:
    #   1. Linking an external image triggers email client warnings
    #   2. Base64 encoded src is not supported by Gmail
    logo_file = os.path.join(os.path.dirname(__file__),
                             "..",
                             "lilium",
                             "static",
                             "img",
                             "pbse-191x32.png")
    with open(logo_file, "rb") as logo:
        logo_mime = MIMEImage(logo.read())
    logo_mime.add_header('Content-ID', '<logo>')
    email.attach(logo_mime)
    email.send(fail_silently=False)


def _run_mailing_list(source: Source,
                      logger: Logger,
                      transformer: Optional[Callable[[Publication], Publication]] = None) -> None:
    """
    Send newly found publications to the mailing list members.
    :param source: scraping data source
    :param logger: source-specific logger
    :param transformer: optional function to modify the publications before sending them
    """
    logger.info("run_mailing_list: {}".format(source.command))
    # Retrieve the members of the mailing list of the specified source
    members = MailingListMember.objects.filter(source=source)
    logger.debug("Mailing list members: {}".format(members))
    # Retrieve the publications to be sent
    if source.last_id is None:
        publications = Publication.objects.filter(source=source)
    else:
        publications = Publication.objects.filter(
            source=source, id__gt=source.last_id)
    logger.info("Publications found: {}".format(len(publications)))
    if not publications:
        logger.info("Nothing to send.")
        return
    # Create the email content
    if transformer:
        publications = [transformer(p) for p in publications]
    recipients = [m.email for m in members]
    send_email(recipients, source.name, publications)
    source.last_id = max(p.id for p in publications)
    logger.info("Email sent; the last publication sent for source {} has ID {}".format(
        source.id, source.last_id))


def _run_scraper_phantomjs(script_file: str,
                           arguments: List[str],
                           source: Source, logger: Logger) -> None:
    """
    Run a PhantomJS-based scraper.
    :param script_file: scraper source code (JavaScript) file name (it must \
                        be located under pbots/tools)
    :param arguments: array of extra arguments to be passed to the script
    :param source: scraping data source
    :param logger: source-specific logger
    """
    tools_dir = os.path.join(os.path.dirname(__file__), "tools")
    script_file = os.path.join(tools_dir, script_file)
    output = subprocess.check_output(
        [settings.PHANTOMJS_EXE, script_file] + arguments)
    # Remove spurious errors
    output = re.findall("\\[.*\\]", output.decode("utf-8"))[0]
    _add_publications(source, logger, output)


def _run_scraper_casperjs(script_file: str,
                          arguments: List[str],
                          source: Source,
                          logger: Logger) -> None:
    """
    Run a CasperJS-based scraper.
    :param script_file: scraper source code (JavaScript) file name (it must \
                        be located under pbots/tools)
    :param arguments: array of extra arguments to be passed to the script
    :param source: scraping data source
    :param logger: source-specific logger
    """
    tools_dir = os.path.join(os.path.dirname(__file__), "tools")
    script_file = os.path.join(tools_dir, script_file)
    output = subprocess.check_output(
        [settings.CASPERJS_EXE, script_file] + arguments)
    _add_publications(source, logger, output)


def _run_scraper_python(script_file: str,
                        arguments: List[str],
                        source: Source,
                        logger: Logger) -> None:
    """
    Run a Python-based scraper.
    :param script_file: scraper source code (Python) file name (it must \
                        be located under pbots/tools)
    :param arguments: array of extra arguments to be passed to the script
    :param source: scraping data source
    :param logger: source-specific logger
    """
    tools_dir = os.path.join(os.path.dirname(__file__), "tools")
    script_file = os.path.join(tools_dir, script_file)
    # Hugly hack to avoid crashes when running under uwsgi
    pyexe = sys.executable
    if pyexe.endswith("uwsgi"):
        pyexe = pyexe[:-len("uwsgi")] + "python"
    output = subprocess.check_output([pyexe, script_file] + arguments)
    _add_publications(source, logger, output)


def _bollettino_regione_umbria_publication_filter(pub: Publication) -> Publication:
    """
    Reset the URLs for Regione Umbria's bulletin publications, since they don't work.
    Besides, the attachments URLs work well.
    :param pub:
    :return:
    """
    pub.url = None
    return pub


def bollettino_regione_umbria_generale(source: Source, logger: Logger) -> None:
    """
    Command to scrape and mail the General series bulletin of Regione Umbria.
    :param source: scraping data source
    :param logger: source-specific logger
    """
    _run_scraper_phantomjs(
        "bollettino-regione-umbria.js", ["1"], source, logger)
    _run_mailing_list(
        source, logger, _bollettino_regione_umbria_publication_filter)


def bollettino_regione_umbria_avvisi(source: Source, logger: Logger) -> None:
    """
    Command to scrape and mail the Announcements series bulletin of Regione Umbria.
    :param source: scraping data source
    :param logger: source-specific logger
    """
    _run_scraper_phantomjs(
        "bollettino-regione-umbria.js", ["2"], source, logger)
    _run_mailing_list(
        source, logger, _bollettino_regione_umbria_publication_filter)


def bollettino_regione_umbria_informazioni(source: Source, logger: Logger) -> None:
    """
    Command to scrape and mail Information series bulletin of Regione Umbria.
    :param source: scraping data source
    :param logger: source-specific logger
    """
    _run_scraper_phantomjs(
        "bollettino-regione-umbria.js", ["3"], source, logger)
    _run_mailing_list(
        source, logger, _bollettino_regione_umbria_publication_filter)


def albopretorio_comune_acquasparta(source: Source, logger: Logger) -> None:
    """
    Command to scrape and mail the general register of Comune di Acquasparta.
    :param source: scraping data source
    :param logger: source-specific logger
    """
    _run_scraper_casperjs(
        "albopretorio-comune-acquasparta.js", [], source, logger)
    _run_mailing_list(source, logger)


def albopretorio_comune_montecastrilli(source: Source, logger: Logger) -> None:
    """
    Command to scrape and mail the general register of Comune di Montecastrilli.
    :param source: scraping data source
    :param logger: source-specific logger
    """
    _run_scraper_python(
        "albopretorio-comune-montecastrilli.py", [], source, logger)
    _run_mailing_list(source, logger)


def matrimoni_comune_montecastrilli(source: Source, logger: Logger) -> None:
    """
    Command to scrape and mail the weddings' register of Comune di Montecastrilli.
    :param source: scraping data source
    :param logger: source-specific logger
    """
    _run_scraper_python(
        "matrimoni-comune-montecastrilli.py", [], source, logger)
    _run_mailing_list(source, logger)


def albopretorio_ic_defilis(source: Source, logger: Logger) -> None:
    """
    Command to scrape and mail the register of the school I. C. "A. De Filis", Terni.
    :param source: scraping data source
    :param logger: source-specific logger
    """
    _run_scraper_casperjs("albopretorio-ic-defilis.js", [], source, logger)
    _run_mailing_list(source, logger)
