import os

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages

from profiles.models import Profile, ProfileAvatar
from profiles.forms import ProfileUpdateForm, UserUpdateForm, AvatarUploadForm
from users.models import User

# Create your views here.


def profile_dashboard(request, pk=None, username=None):
    profile = Profile.objects.select_related('user').get(pk=pk)
    avatar = ProfileAvatar.objects.select_related(
        'profile').get(profile_id=profile.id)

    context = {
        'profile': profile,
        'avatar': avatar,
    }
    return render(request, 'profiles/profile_dashboard.html', context)


def profile_update(request, pk=None, username=None):
    profile = Profile.objects.select_related('user').get(pk=pk)
    avatar = ProfileAvatar.objects.select_related(
        'profile').get(profile_id=profile.id)

    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, instance=profile)
        av_form = AvatarUploadForm(
            request.POST, request.FILES, instance=profile)
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
        av_form = AvatarUploadForm(instance=profile)

    context = {
        'avatar': avatar,
        'form': form,
        'av_form': av_form,
        'profile': profile,
    }
    return render(request, 'profiles/profile_update.html', context)


def user_update(request, pk=None, username=None):
    user = User.objects.get(pk=pk)
    profile = Profile.objects.select_related('user').get(pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=profile.user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            messages.success(request, 'Update Successful')
            return HttpResponseRedirect(reverse('profiles:update', kwargs={'pk': pk, 'username': username}))
        else:
            messages.warning(
                request, 'There was an error with your submission.')
    else:
        form = UserUpdateForm(instance=profile.user)
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profiles/user_update.html', context)


def avatar_upload(request, pk, username):
    user = User.objects.get(pk=pk)
    profile = Profile.objects.select_related('user').get(pk=pk)
    avatar = ProfileAvatar.objects.select_related(
        'profile').get(profile_id=profile.id)
    try:
        if request.FILES['avatar']:
            if avatar.avatar.name != 'generic/default.jpg':
                avatar.avatar.delete(save=False)

            avatar.avatar = request.FILES['avatar']
            avatar.save()
            messages.success(request, 'Update Successful')
        else:
            messages.warning(
                request, 'There was an error with your submission.')
    except:
        messages.warning(request, 'There was an error with your submission.')

    return HttpResponseRedirect(reverse('profiles:edit', kwargs={'pk': pk, 'username': username}))
