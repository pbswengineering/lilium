# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
migrations.0001_initial
~~~~~~~~~~~~~~~~~~~~~~~

Create the base tables for sensors and their readings.

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Create the Sensor and SensorReading tables.
    """

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=256)),
                ('specs', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='SensorReading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tstamp', models.DateTimeField()),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('humidity', models.FloatField(blank=True, null=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cecilia.Sensor')),
            ],
        ),
    ]
