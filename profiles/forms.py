#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, Button, Reset, Div
from crispy_forms.bootstrap import FormActions, PrependedText

from profiles.models import Profile
from users.models import User


class ProfileUpdateForm(ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'rows': 10, 'cols': 20, 'style': 'resize:none', 'max_length': 140}))

    class Meta:
        model = Profile
        fields = ['bio', 'location']

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if bio:
            if len(bio) > 140:
                raise forms.ValidationError(
                    _('You have exceeded the maximum length of 140 characters.'), code='profile_bio_long')

        return bio

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'updateProfile'
        self.helper.form_method = 'post'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Div(
                Div(Field('bio', placeholder='Add a bio.',
                          active=True, css_class='col-md-12', style='margin: 2px 0 10px 0;')),
                Div(Field('location', placeholder='Enter City/Town/State',
                          active=True, css_class='col-md-12', style='margin: 2px 0 10px 0;')),
                Div(FormActions(Submit('submit', 'Submit',
                                       css_class='btn btn-success')), css_class='col-md-12', style='margin-top:10px;'),
                css_class='col-md-12', style='margin-top:50px;',
            ),
        )
