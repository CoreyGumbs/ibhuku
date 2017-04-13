#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from profiles.models import Profile, ProfileAvatar


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def create_profile_avatar(sender, instance, created, **kwargs):
    if created:
        ProfileAvatar.objects.create(profile=instance)


@receiver(post_save, sender=Profile)
def save_profile_avatar(sender, instance, **kwargs):
    instance.profileavatar.save()
