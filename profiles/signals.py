#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

from PIL import Image, ImageOps
from io import StringIO, BytesIO

from django.db.models import ImageField
from django.apps import apps
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.files.base import ContentFile


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


@receiver(pre_save, sender=ProfileAvatar)
def profile_image_resize(sender, instance, **kwargs):
    ext = instance.avatar.name.split('.')[-1]
    image = Image.open(instance.avatar)
    image_resize = ImageOps.fit(image, (300, 300), Image.LANCZOS)

    image_resize_io = BytesIO()
    if ext in ['jpg', 'jpeg']:
        image_resize.save(image_resize_io, format='JPEG')
    elif ext in ['png']:
        image_resize.save(image_resize_io, format='PNG')

    temp_name = instance.avatar.name

    instance.avatar.save(temp_name, content=ContentFile(
        image_resize_io.getvalue()), save=False)
