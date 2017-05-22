from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy

from profiles import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/(?P<username>[-\w\d_]+)$',
        views.profile_dashboard, name='dashboard'),
    url(r'^settings/(?P<pk>[0-9]+)/(?P<username>[-\w\d_]+)$',
        views.profile_update, name='edit'),
    url(r'^settings/user/(?P<pk>[0-9]+)/(?P<username>[-\w\d_]+)$',
        views.user_update, name='update'),
    url(r'^settings/user/upload/(?P<pk>[0-9]+)/(?P<username>[-\w\d_]+)$',
        views.avatar_upload, name='av-upload'),
    url(r'^settings/user/social-media/(?P<pk>[0-9]+)/(?P<username>[-\w\d_]+)$',
        views.social_media_links, name='socials'),
]
