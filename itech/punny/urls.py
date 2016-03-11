from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from punny import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^search/$', views.search, name='search'),
                       url(r'^settings/$', views.settings, name='settings'),
                       url(r'^tag/(?P<tag_name_slug>[\w\-]+)/$', views.tag_detail, name='tag_detail'),
                       url(r'^profile/(?P<username>[\w\-]+)/$', views.user_profile, name='profile'),
                       )  # search should be updated to include the actual search value
