#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

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
                'max_length': 140,
            })
        }

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if bio:
            if len(bio) > 140:
                raise forms.ValidationError(
                    _('You have exceeded the maximum character length of 140.'), code='profile_bio_long')

        return bio
