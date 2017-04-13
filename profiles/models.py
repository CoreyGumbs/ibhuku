from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Create your models here.

# user image/avatar directory path
def user_directory_path(instance, filename):
    """
    User Profile Avatar Uploaded Directory Path.
    """
    return 'user_{0}/avatar/{1}'.format(instance.profile.user.id, filename)


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
        Profile, on_delete=models.CASCADE, primary_key=True)
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
