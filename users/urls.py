from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from users.views import CreateUserAccountView, ConfirmAccountEmailActivationLink

urlpatterns = [
    url(r'^$', RedirectView.as_view(
        url=reverse_lazy('users:register')), name='index'),
    url(r'^register/$', CreateUserAccountView, name='register'),
    url(r'^activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ConfirmAccountEmailActivationLink, name='activation')
]
