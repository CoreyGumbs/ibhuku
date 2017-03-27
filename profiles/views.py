from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from profiles.models import Profile
from users.models import User

# Create your views here.


def profile_dashboard(self, pk=None):
    user = pk
    return HttpResponse('hello' + user)
