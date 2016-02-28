from django.conf.urls import patterns, url
from punny import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))