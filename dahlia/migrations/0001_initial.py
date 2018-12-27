# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
migrations.0001_initial
~~~~~~~~~~~~~~~~~~~~~~~

Create the base tables to manage documents, categories and revisions.

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Create the tables for documents, categories and revisions.
    """

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dahlia.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=191, unique=True)),
                ('title', models.CharField(max_length=2048)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dahlia.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=191)),
                ('tstamp', models.DateTimeField()),
                ('description', models.CharField(max_length=4096)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
