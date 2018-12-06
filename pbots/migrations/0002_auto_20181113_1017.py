# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
migrations.0002_auto_20181113_1017
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the supported scraping data sources and subscribe Paolo Bernardi
to each one of them.

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.db import migrations


def insert_default_sources(apps, schema_editor) -> None:
    """
    Configure the supported scraping data sources.
    :param apps:
    :param schema_editor:
    """
    Source = apps.get_model("pbots", "Source")
    Source(id=1, name="Albo Pretorio del Comune di Acquasparta", command="albopretorio_comune_acquasparta").save()
    Source(id=2, name="Albo Pretorio del Comune di Montecastrilli", command="albopretorio_comune_montecastrilli").save()
    Source(id=3, name="Bollettino della Regione Umbria, serie generale", command="bollettino_regione_umbria_generale").save()
    Source(id=4, name="Bollettino della Regione Umbria, serie avvisi e concorsi", command="bollettino_regione_umbria_avvisi").save()
    Source(id=5, name="Bollettino della Regione Umbria, serie informazioni e comunicazione", command="bollettino_regione_umbria_informazioni").save()


def insert_default_ml_members(apps, schema_editor) -> None:
    """
    Add Paolo Bernardi as member for the mailing lists of the above-mentioned data sources.
    :param apps:
    :param schema_editor:
    """
    MailingListMember = apps.get_model("pbots", "MailingListMember")
    # Mailing list Albo Pretorio del Comune di Acquasparta
    MailingListMember(name="Paolo Bernardi", email="paolo@bernardi.cloud", source_id=1).save()
    # Mailing list Albo Pretorio del Comune di Montecastrilli
    MailingListMember(name="Paolo Bernardi", email="paolo@bernardi.cloud", source_id=2).save()
    # Mailing list Bollettino della Regione Umbria, serie generale
    MailingListMember(name="Paolo Bernardi", email="paolo@bernardi.cloud", source_id = 3).save()
    # Mailing list Bollettino della Regione Umbria, serie avvisi e concorsi
    MailingListMember(name="Paolo Bernardi", email="paolo@bernardi.cloud", source_id = 4).save()
    # Mailing list Bollettino della Regione Umbria, serie informazioni e comunicazione
    MailingListMember(name="Paolo Bernardi", email="paolo@bernardi.cloud", source_id = 5).save()


class Migration(migrations.Migration):
    """
    Configure the supported scraping data sources and add Paolo Bernardi as member
    for the mailing lists of the above-mentioned data sources.
    """
    dependencies = [
        ("pbots", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(insert_default_sources),
        migrations.RunPython(insert_default_ml_members),
    ]
