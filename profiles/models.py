import os
from PIL import Image, ImageOps
from io import BytesIO

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile


# user image/avatar directory path
def user_directory_path(instance, filename):
    """
    User Profile Avatar Uploaded Directory Path.
    """
    ext = filename.split('.')[-1]
    new_name = '{0}_{1}.{2}'.format(
        'profile', instance.profile.user.username, ext)
    return 'user_{0}_profile/avatar/{1}'.format(instance.profile.user.id, new_name)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(_('bio'), max_length=140, blank=True)
    location = models.CharField(_('location'), max_length=140, blank=True)
    url_name = models.CharField(
        _('profile URL'), max_length=150, blank=True, unique=True)
    email_confirmed = models.BooleanField(_('confirmed'), default=False)
    current_occupation = models.CharField(
        _('occupation'), max_length=255, blank=True)

    class Meta:
        db_table = 'profile'
        verbose_name = _('profile')
        verbose_name_plural = _('user_profiles')

    def user_url_name(self):
        return '{0}{1}'.format('@', self.url_name)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username


class ProfileAvatar(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_directory_path, default='generic/default.jpg')
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'avatars'
        verbose_name = _('avatars')
        verbose_name_plural = _('profile_avatars')

    def __unicode__(self):
        return self.avatar

    def __str__(self):
        return str(self.avatar)

    def save(self, *args, **kwargs):
        ext = self.avatar.name.split('.')[-1]
        image = Image.open(self.avatar)
        image_resize = ImageOps.fit(image, (300, 300), Image.LANCZOS)

        image_resize_io = BytesIO()
        if ext in ['jpg', 'jpeg']:
            image_resize.save(image_resize_io, format='JPEG')
        elif ext in ['png']:
            image_resize.save(image_resize_io, format='PNG')

        temp_name = self.avatar.name
        self.avatar.save(temp_name, content=ContentFile(
            image_resize_io.getvalue()), save=False)
        super(ProfileAvatar, self).save(*args, **kwargs)


class ProfileSocial(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE)
    facebook = models.URLField(_('facebook'), max_length=2000, blank=True)
    twitter = models.URLField(_('twitter'), max_length=2000, blank=True)
    google = models.URLField(_('google'), max_length=2000, blank=True)
    linkedin = models.URLField(_('linkedin'), max_length=2000, blank=True)
    instagram = models.URLField(_('instagram'), max_length=2000, blank=True)
    pintrest = models.URLField(_('pintrest'), max_length=2000, blank=True)
    website = models.URLField(_('website'), max_length=2000, blank=True)

    class Meta:
        db_table = 'profile_social_links'
        verbose_name = _('social_link')
        verbose_name_plural = _('social_links')

    def __unicode__(self):
        return self.profile.user.username

    def __str__(self):
        return self.profile.user.username
