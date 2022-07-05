# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

app_name = 'dwsyahoo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^question_id/$', views.detail, name='detail'),
    url(r'^convert_csv/$', views.convert_csv, name='convert_csv'),
]