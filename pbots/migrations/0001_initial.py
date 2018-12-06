# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
migrations.0001_initial
~~~~~~~~~~~~~~~~~~~~~~~

Create the base tables for mailing lists, publications and scraping
data sources.

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Create the Source, MailingListMember, Publication and PublicationAttachment tables.
    """

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailingListMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=2048, null=True)),
                ('number', models.CharField(blank=True, max_length=256, null=True)),
                ('publisher', models.CharField(blank=True, max_length=256, null=True)),
                ('pub_type', models.CharField(blank=True, max_length=256, null=True)),
                ('subject', models.CharField(blank=True, max_length=2048, null=True)),
                ('date_start', models.CharField(blank=True, max_length=256, null=True)),
                ('date_end', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('url', models.CharField(max_length=2048)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pbots.Publication')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID',
                                        unique=True)),
                ('name', models.CharField(max_length=256)),
                ('command', models.CharField(max_length=1024)),
                ('running', models.BooleanField(default=False)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('executions', models.IntegerField(default=0)),
                ('last_execution_ok', models.BooleanField(default=True)),
                ('last_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='publication',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pbots.Source'),
        ),
        migrations.AddField(
            model_name='mailinglistmember',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pbots.Source'),
        ),
    ]
