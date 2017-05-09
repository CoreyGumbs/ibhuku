#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PIL import Image, ImageOps
from io import StringIO, BytesIO

from django.db.models import ImageField
from django.apps import apps
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.files.base import ContentFile


from users.models import User
from profiles.models import Profile, ProfileAvatar, ProfileSocial


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="profile_create")
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="profile_save")
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile, dispatch_uid="profile_social_create")
def create_profile_social(sender, instance, created, **kwargs):
    if created:
        ProfileSocial.objects.create(profile=instance)


@receiver(post_save, sender=Profile, dispatch_uid="profile_social_save")
def save_profile_social(sender, instance, **kwargs):
    if kwargs['created']:
        instance.profilesocial.save()


@receiver(post_save, sender=Profile, dispatch_uid="profile_avatar_create")
def create_profile_avatar(sender, instance, created, **kwargs):
    if created:
        ProfileAvatar.objects.create(profile=instance)
