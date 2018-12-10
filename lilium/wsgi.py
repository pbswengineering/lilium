"""
lilium.wsgi
~~~~~~~~~~~

WSGI configuration for the Lilium project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lilium.settings')

# pylint: disable=invalid-name
# Rationale:
#   - This is a WSGI standard name.
application = get_wsgi_application()
