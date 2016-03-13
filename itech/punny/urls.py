from django.conf.urls import patterns, url, include
from django.views.generic.base import RedirectView
from punny import views
from updown.views import AddRatingFromModel
from watson import search as watson

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^settings/$', views.settings, name='settings'),
                       url(r'^tag/(?P<tag_name_slug>[\w|\W\-]+)/$', views.tag_detail, name='tag_detail'),
                       url(r'^profile/(?P<username>[\w\-]+)/$', views.user_profile, name='profile'),
                       url(r"^(?P<object_id>\d+)/rate/(?P<score>[\d\-]+)$", AddRatingFromModel(), {
                           'app_label': 'punny',
                           'model': 'Pun',
                           'field_name': 'rating',
                       }, name="pun_rating"),
                       url(r'^search/$', views.search, name="search"),
                       url(r"^search-results/", include("watson.urls", namespace="watson")),
                       url(r'^accounts/', include('registration.backends.simple.urls'),))  # search should be updated to include the actual search value
