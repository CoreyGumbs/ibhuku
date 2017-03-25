from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'profile'
        verbose_name = _('profile')
        verbose_name_plural = _('user_profiles')

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username
