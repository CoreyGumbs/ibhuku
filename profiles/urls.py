from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy

from profiles import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.profile_dashboard, name='dashboard'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.profile_update, name='update'),
]
