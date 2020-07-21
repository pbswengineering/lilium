# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
lilium.urls
~~~~~~~~~~~

URL configuration for Lilium. It includes URL configuration from
sub-applications (admin, cecilia, pbots...) and some defaults.

For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

:copyright: (c) 2018 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

# pylint: disable=invalid-name
# Rationale:
#   - urlpatterns is a Django standard name.

urlpatterns = [
    path("cecilia/", include("cecilia.urls")),
    path("dahlia/", include("dahlia.urls")),
    path("pbots/", include("pbots.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    # By default show the PBOTS status
    path("", RedirectView.as_view(url="/pbots/")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
