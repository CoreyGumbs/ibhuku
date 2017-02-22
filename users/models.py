from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _


from users.managers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(_('first name'), max_length=100, blank=False)
	last_name = models.CharField(_('last name'),max_length=100, blank = True)
	username = models.CharField(_('username'), max_length=50, unique=True, blank=True)
	email =  models.EmailField(_('email'),max_length=255, unique=True, blank=False)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	last_login = models.DateTimeField(_('last login'), auto_now=True)
	is_active =  models.BooleanField(_('active'), default=False)
	is_staff = models.BooleanField(_('staff'), default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name']

	class Meta:
		db_table = 'users'
		verbose_name = _('user')
		verbose_name_plural = _('users') 

	def get_full_name(self):
		if self.last_name:
			return '{0}{1}'.format(self.first_name[:1], self.last_name)
		else:
			return self.first_name

	def get_short_name(self):
		if self.last_name:
			return '{0}{1}'.format(self.first_name[:1], self.last_name)
		else:
			return self.first_name

	def __unicode__(self):
		if self.last_name:
			return '{0}{1}'.format(self.first_name[:1], self.last_name)
		else:
			return self.first_name

	def __str__(self):
		if self.last_name:
			return '{0}{1}'.format(self.first_name[:1], self.last_name)
		else:
			return self.first_name

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')

	class Meta:

		db_table = 'profiles'
		verbose_name = _('profile')
		verbose_name_plural = _('profiles')

	def __unicode__(self):
		return self.user.get_full_name()

	def __str__(self):
		return self.user.get_full_name()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


