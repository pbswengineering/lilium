# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
pbots.models
~~~~~~~~~~~~

Models to manage scraping data sources, publications and mailing lists.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.db import models
from django.utils import timezone


class Source(models.Model):
    """
    Scraping data source.
    """
    name = models.CharField(max_length=256)
    command = models.CharField(max_length=1024)
    running = models.BooleanField(default=False)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    executions = models.IntegerField(default=0)
    last_execution_ok = models.BooleanField(default=True)
    last_id = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the Source
        :return: the source name
        """
        return self.name

    def mark_start(self) -> None:
        """
        Record the start of the scraping for this source (set start time and clear end time).
        """
        self.running = True
        self.started_at = timezone.now()
        self.finished_at = None
        self.executions = self.executions + 1
        self.save()

    def mark_stop(self) -> None:
        """
        Record the stop of the scraping for this source.
        """
        self.running = False
        self.finished_at = timezone.now()
        self.save()


class MailingListMember(models.Model):
    """
    Member of a mailing list (a person with an email address).
    Please note that there isn't a MailingList model, mailing list members
    are directly associated to a Source (which corresponds to a ML).
    """
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the mailing list member.
        :return: the member email and the Source/ML that he's associated to
        """
        return "{} on {}".format(self.email, self.source)


class Publication(models.Model):
    """
    Publication of a register (or a website, in general).
    """
    # pylint: disable=too-many-instance-attributes
    # Rationale:
    #   - It just reflects the underlying table data model, which is normalised.
    url = models.CharField(max_length=2048, blank=True, null=True)
    number = models.CharField(max_length=256, blank=True, null=True)
    publisher = models.CharField(max_length=256, blank=True, null=True)
    pub_type = models.CharField(max_length=256, blank=True, null=True)
    subject = models.CharField(max_length=2048, blank=True, null=True)
    date_start = models.CharField(max_length=256, blank=True, null=True)
    date_end = models.CharField(max_length=256, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the publication.
        :return: a human-readable string representation of the publication
        """
        return "{} - {} ({})".format(self.publisher, self.subject, self.date_start)


class PublicationAttachment(models.Model):
    """
    Attachment of a register's publication.
    """
    name = models.CharField(max_length=1024)
    url = models.CharField(max_length=2048)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the attachment.
        :return: the name of the attachment
        """
        return self.name
