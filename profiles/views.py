from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages

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
    profile = Profile.objects.select_related('user').get(pk=pk)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profiles/profile_update.html', context)
