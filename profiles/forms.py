#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import string

from django import forms
from django.forms import ModelForm, Textarea, TextInput
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, Button, Reset, Div, HTML
from crispy_forms.bootstrap import FormActions, PrependedText

from profiles.models import Profile
from users.models import User


class ProfileUpdateForm(ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'id': 'bio_field', 'rows': 5, 'style': 'resize: none', 'maxlength': 140}))

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'current_occupation', 'url_name']
        widget = {
            'url_name': TextInput(attrs={'maxlength': 15}),
        }

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if bio is not None:
            if len(bio) > 140:
                raise forms.ValidationError(
                    _('The maximum length of characters is 140.'), code='profile_bio_long')

        return bio

    def clean_url_name(self):
        url_name = ''.join(self.cleaned_data['url_name'].split())
        # symbol = [c for c in url_name if c in string.punctuation]
        # translator = str.maketrans('_', '-', string.punctuation)
        # url = url_name.translate(translator)

        if url_name:
            if len(url_name) > 15:
                raise forms.ValidationError(
                    _('The maximum length of characters is 15.'),
                    code='profile_url_long')
        return url_name

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'updateProfile'
        self.helper.form_method = 'post'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Div(
                Div(Field('bio', placeholder='Add a bio.',
                          active=True, css_class='col-md-12')),
                Div(HTML('''
                    <span id="bio_character_feedback">140</span>'''),
                    style='width: 190px; margin:0 0 5px 120px; color: #b6b6b6; padding:0; text-align: right; float:right; clear: both;',
                    css_class='col-xs-12'),
                Div(PrependedText('url_name', 'ibhuku.com/',
                                  placeholder='Enter a name. ')),
                Div(Field('location', placeholder='Enter City/Town/State',
                          active=True, css_class='col-md-12')),
                Div(Field('current_occupation', placeholder='Enter current occupation',
                          active=True, css_class='col-md-12')),
                Div(FormActions(Submit('submit', 'Submit',
                                       css_class='btn btn-success')), style='padding:0;', css_class='col-md-12'),
                css_class='col-md-12', style='padding:0',
            ),
        )


class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
