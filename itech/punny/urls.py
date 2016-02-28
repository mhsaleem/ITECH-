from django.conf.urls import patterns, url
from punny import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^search/$', views.search, name='search'),) #search should be updated to include the actual search value