#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.forms import ModelForm, Textarea
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
                Div(PrependedText('url_name', 'ibhuku.com/', placeholder='')),
                Div(Field('location', placeholder='Enter City/Town/State',
                          active=True, css_class='col-md-12')),
                Div(Field('current_occupation', placeholder='Enter Current Occupation',
                          active=True, css_class='col-md-12')),
                Div(FormActions(Submit('submit', 'Submit',
                                       css_class='btn btn-success')), style='padding:0;', css_class='col-md-12'),
                css_class='col-md-12', style='padding:0',
            ),
        )
