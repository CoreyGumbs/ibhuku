from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(max_length=100, blank=False)
	last_name = models.CharField(max_length=100, blank = True)