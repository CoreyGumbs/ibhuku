#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import string
from PIL import Image, ImageOps

from django import forms
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.images import ImageFile
from django.forms import ModelForm, Textarea, TextInput
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, Button, Reset, Div, HTML
from crispy_forms.bootstrap import FormActions, PrependedText

from profiles.models import Profile, ProfileAvatar
from profiles.profilelib.strip_url import strip_punctuation
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
        url = strip_punctuation(url_name)

        if url_name:
            if len(url_name) > 15:
                raise forms.ValidationError(
                    _('The maximum length of characters is 15.'), code='url_name_punc_error')

        return url

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
                                       css_class='btn btn-success', css_id='updateSubmit')), style='padding:0;', css_class='col-md-12'),
                css_class='col-md-12', style='padding:0',
            ),
        )


class UserUpdateForm(ModelForm):
    first_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def clean_username(self):
        username = self.cleaned_data['username']
        new_username = strip_punctuation(username)

        if username:
            if len(username) > 15:
                raise forms.ValidationError(
                    _('The maximum length of characters is 15.'), code='username_len_error')

        return new_username

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'updateUser'
        self.helper.form_method = 'post'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Div(
                Div(Field('first_name', placeholder='First name',
                          active=True, css_class='col-md-6')),
                Div(Field('last_name', placeholder='Last name',
                          active=True, css_class='col-md-6')),
                Div(Field('email', placeholder='Email',
                          active=True, css_class='col-md-12')),
                Div(Field('username', placeholder='Username',
                          active=True, css_class='col-md-12')),
                Div(FormActions(Submit('submit', 'Submit',
                                       css_class='btn btn-success', css_id='updateSubmit')), style='padding:0;', css_class='col-md-12'),
                css_class='col-md-12', style='padding:0',
            ),
        )


class AvatarUploadForm(ModelForm):

    class Meta:
        model = ProfileAvatar
        fields = ['avatar']

    def clean_avatar(self):
        image = self.cleaned_data['avatar']
        new_img = Image.open(image)

        if getattr(new_img, 'format') not in ['JPEG', 'JPG', 'PNG']:
            raise forms.ValidationError(
                _('Only .jpg or .png file formats are supported.'), code='wrong_file_format')
        return image

    def __init__(self, *args, **kwargs):
        super(AvatarUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'forms-inline'
        self.helper.form_id = 'avatarUpload'
        self.helper.form_method = 'post'
        # self.helper.form_action = reverse(
        #     'profiles:av-upload', kwargs={'pk': self.instance.pk, 'username': self.instance.user.username})
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Div(Div(Field('avatar', placeholder='Upload Profile',
                          active=True, css_class='col-md-6')),
                Div(FormActions(Submit('submit', 'Submit',
                                       css_class='btn btn-success', css_id='updateSubmit')), style='padding:0;', css_class='col-md-12'),
                css_class='col-md-12', style='padding:0',
                ),
        )
