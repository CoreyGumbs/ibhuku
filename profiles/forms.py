#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.forms import ModelForm

from profiles.models import Profile
from users.models import User


class ProfileUpdateForm(ModelForm):
    bio = forms.CharField()

    class Meta:
        model = Profile
        fields = ('bio', 'location',)
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 10,
                'columns': 20,
                'style': 'resize:none;',
                'max_length': 150
            })
        }
