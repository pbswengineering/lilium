# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
dahlia.models
~~~~~~~~~~~~~

Models to manage documents and their metadata.

:copyright: (c) 2018 Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    """
    A category is a way of classifying documents. Each documents belongs
    to a specific category and to all ancestor categories.
    """
    name = models.CharField(max_length=256)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        """
        Django makes plurals just by appending an "s".
        """
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the Category.
        :return: the category name
        """
        full_name = self.name
        obj = self
        if obj.parent:
            full_name = "{} / {}".format(str(self.parent), full_name)
        return full_name


class Document(models.Model):
    """
    A document is a text (or possibly any other media) on a specific
    topic.
    """
    # MySQL does not allow unique CharFields to have a max_length > 255
    # However, with utf8mb4 max_length becomes 191:
    # https://stackoverflow.com/questions/1814532/1071-specified-key-was-too-long-max-key-length-is-767-bytes
    identifier = models.CharField(max_length=191, unique=True)
    title = models.CharField(max_length=2048)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the Document.
        :return: the document identifier and title
        """
        return "{}: {}".format(self.identifier, self.title)


class Revision(models.Model):
    """
    A document has zero or more revisions. Each revision of a document
    corresponds to a file (usually a written file, but any media could
    be supported, in principle) and some metadata.
    """
    identifier = models.CharField(max_length=191)
    tstamp = models.DateTimeField()
    description = models.CharField(max_length=4096)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class File(models.Model):
    """
    A revision has zero or more files. Each file is stored in the
    local file system.
    """
    path = models.CharField(max_length=1024)
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE)
