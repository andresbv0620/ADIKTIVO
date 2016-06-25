# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import patterns, url

from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    #url(r'^ajax/add/$', ajax.add_todo),
    #url(r'^ajax/more/$', ajax.more_todo),
    url(r'^ajax/$', TemplateView.as_view(template_name="alertas/index.html")),
    url(r'^match/$', views.check_match),

        # URL pattern for the AlertView
    url(
        regex=r'^create/$',
        view=views.AlertView.as_view(),
        name='create'
    ),
]
