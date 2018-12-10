# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
migrations.0002_auto_20181114_1447
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the default sensors of Cecilia.

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.db import migrations


def insert_default_sensors(apps, schema_editor) -> None:
    """
    Add the default Cecilia's sensors to the Sensor table.
    :param apps:
    :param schema_editor:
    """
    # pylint: disable=unused-argument,invalid-name
    # Rationale:
    #   - This is the default signature of ORM RunPython operations.
    #   - The "Sensor" variable is a class name.
    Sensor = apps.get_model("cecilia", "Sensor")
    Sensor(id=1, name="living_room", type="DHT22", specs="Temp. ± 0.5° / Humidity ± 2%").save()
    Sensor(id=2, name="attic", type="DHT22", specs="Temp. ± 0.5° / Humidity ± 2%").save()
    Sensor(id=3, name="basement", type="DHT22", specs="Temp. ± 0.5° / Humidity ± 2%").save()


class Migration(migrations.Migration):
    """
    Add the default Cecilia's sensors to the Sensor table.
    """
    dependencies = [
        ('cecilia', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(insert_default_sensors)
    ]
