#!/usr/bin/env python

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password

from users.models import User

class UserRegistrationForm(ModelForm):
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'password', 'acct_type', 'toc')
		#fields_required = ('first_name', 'last_name', 'email')