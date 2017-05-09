#!/usr/bin/env python

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, Button, Reset, Div
from crispy_forms.bootstrap import FormActions, PrependedText

from users.models import User
from users.choices import ACCOUNT_TYPE


class UserRegistrationForm(ModelForm):
    last_name = forms.CharField(label='Last Name', required=True)
    password = forms.CharField(
        label='Password', required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label='Confirm Password', required=True, widget=forms.PasswordInput())
    acct_type = forms.ChoiceField(label='I Am:', required=True, widget=forms.Select(
        attrs={'value': 'IND'}), choices=ACCOUNT_TYPE)
    toc = forms.BooleanField(
        label='I agree to the < a href="#" > terms and conditions < /a > of Ibuku.com', required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'password', 'acct_type', 'toc',)
        fields_required = ('first_name', 'last_name', 'email',
                           'password', 'acct_type', 'toc',)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'registerForm'
        self.helper.form_method = 'post'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Div(
                Div(Field('first_name', placeholder="First Name",
                          active=True), css_class='col-xs-6'),
                Div(Field('last_name', placeholder="Last Name",
                          active=True), css_class='col-xs-6'),
                Div(Field('email', placeholder="Email",
                          active=True), css_class='col-md-12'),
                Div(Field('password', placeholder="Password",
                          active=True), css_class='col-xs-6'),
                Div(Field('confirm_password', placeholder="Confirm Password",
                          active=True), css_class='col-xs-6'),
                Div(Field('acct_type', active=True), css_class='col-md-12'),
                Div(FormActions(Submit('submit', 'Submit',
                                       css_class='btn btn-success btn-lg btn-block')), css_class='col-md-12'),
                Div(Field('toc', active=True), css_class='col-xs-12'),
                css_class='col-md-12', style='margin-top:50px;',
            ),
        )

    def clean_password(self):
        password = self.cleaned_data['password']
        if password:
            if len(password) < 8:
                raise forms.ValidationError(
                    _('Password must be at least 8 characters.'), code='password_short')
        return password

    def clean(self):
        self.cleaned_data = super(UserRegistrationForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                _("Passwords don't match. Please check and try again."),
                code='pass_invalid_match')

        return self.cleaned_data


class ResendActivationLinkForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super(ResendActivationLinkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'resendlinkForm'
        self.helper.form_method = 'post'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Div(
                Div(Field(
                    'email', placeholder="Email",
                    active=True, css_class='col-md-3'),
                    ),
                Div(
                    FormActions(
                        Submit('submit', 'Submit', css_class='col-md-3')
                    )
                ),
                css_class='col-md-12',
            ),
        )
