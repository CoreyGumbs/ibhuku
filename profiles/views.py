from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from profiles.models import Profile
from profiles.forms import ProfileUpdateForm
from users.models import User

# Create your views here.


def profile_dashboard(request, pk=None):
    profile = Profile.objects.select_related('user').get(pk=pk)
    context = {
        'profile': profile,
    }
    return render(request, 'profiles/profile_dashboard.html', context)


def profile_update(request, pk=None):
        # Need to make each user update field their own form for saving.
    profile = Profile.objects.select_related('user').get(pk=pk)
    form = ProfileUpdateForm()
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profiles/profile_update.html', context)
