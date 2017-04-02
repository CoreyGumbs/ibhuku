from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Create your models here.


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
