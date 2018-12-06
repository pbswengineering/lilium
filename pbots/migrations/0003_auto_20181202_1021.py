# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
migrations.0003_auto_20181202_1021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the following scraping sources and subscribe Paolo Bernardi
to their mailing lists:
  - Weddings of "Comune di Montecastrilli"
  - Register of I. C. "A. De Filis", Terni

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.db import migrations


def insert_default_sources(apps, schema_editor) -> None:
    """
    Add the scraping data sources for Weddings of "Comune di Montecastrilli" and "I. C. 'A. De Filis'".
    :param apps:
    :param schema_editor:
    """
    Source = apps.get_model("pbots", "Source")
    Source(id=6, name="Albo Pretorio dell'I. C. \"A. De Filis\", Terni", command="albopretorio_ic_defilis").save()
    Source(id=7, name="Matrimoni del Comune di Montecastrilli", command="matrimoni_comune_montecastrilli").save()


def insert_default_ml_members(apps, schema_editor) -> None:
    """
    Add Paolo Bernardi to the MLs for Weddings of "Comune di Montecastrilli" and "I. C. 'A. De Filis'".
    :param apps:
    :param schema_editor:
    """
    MailingListMember = apps.get_model("pbots", "MailingListMember")
    # Mailing list Albo Pretorio dell'I. C. "A. De Filis", Terni
    MailingListMember(name="Paolo Bernardi", email="paolo@bernardi.cloud", source_id=6).save()
    # Mailing list Matrimoni del Comune di Montecastrilli
    MailingListMember(name="Paolo Bernardi", email="paolo@bernardi.cloud", source_id=7).save()


class Migration(migrations.Migration):
    """
    Add the scraping data sources for Weddings of "Comune di Montecastrilli" and "I. C. 'A. De Filis'" and
    subscribe Paolo Bernardi to their mailing lists.
    """
    dependencies = [
        ("pbots", "0002_auto_20181113_1017"),
    ]

    operations = [
        migrations.RunPython(insert_default_sources),
        migrations.RunPython(insert_default_ml_members),
    ]
