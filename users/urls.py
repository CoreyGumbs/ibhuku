from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from users.views import CreateUserAccountView

urlpatterns = [
	url(r'^$', RedirectView.as_view(url=reverse_lazy('users:register')), name='index'),
	url(r'^register/$', CreateUserAccountView, name='register'),
]