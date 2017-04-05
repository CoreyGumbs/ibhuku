from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages

from profiles.models import Profile
from profiles.forms import ProfileUpdateForm, UserUpdateForm
from users.models import User

# Create your views here.


def profile_dashboard(request, pk=None, username=None):
    profile = Profile.objects.select_related('user').get(pk=pk)
    context = {
        'profile': profile,
    }
    return render(request, 'profiles/profile_dashboard.html', context)


def profile_update(request, pk=None, username=None):
    profile = Profile.objects.select_related('user').get(pk=pk)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            messages.success(request, 'Update Successful')
            return HttpResponseRedirect(reverse('profiles:edit', kwargs={'pk': pk, 'username': username}))
        else:
            messages.warning(
                request, 'There was an error with your submission.')
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profiles/profile_update.html', context)


def user_update(request, pk=None, username=None):
    profile = Profile.objects.select_related('user').get(pk=pk)
    form = UserUpdateForm()
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profiles/user_update.html', context)
