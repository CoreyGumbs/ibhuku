from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy

from profiles import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/(?P<username>[-\w\d_]+)/$',
        views.profile_dashboard, name='dashboard'),
    url(r'^edit/(?P<pk>[0-9]+)/(?P<username>[-\w\d_]+)/$',
        views.profile_update, name='edit'),
    url(r'^update/(?P<pk>[0-9]+)/(?P<username>[-\w\d_]+)/$',
        views.user_update, name='update'),
]
