from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(_('bio'), max_length=140, blank=True)
    location = models.CharField(_('location'), max_length=255, blank=True)
    email_confirmed = models.BooleanField(_('confirmed'), default=False)

    class Meta:
        db_table = 'profile'
        verbose_name = _('profile')
        verbose_name_plural = _('user_profiles')

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username
