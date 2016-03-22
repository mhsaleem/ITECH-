from django.conf.urls import patterns, url, include
import views
from updown.views import AddRatingFromModel
from registration.backends.simple.views import RegistrationView
from django.contrib import admin

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/punny/settings/'

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
                       url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
                       url(r'^accounts/', include('registration.backends.simple.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
