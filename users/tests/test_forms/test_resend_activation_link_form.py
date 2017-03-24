#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import factory
import factory.django

from users.tests.factories import UserFactory
from users.models import User
from users.forms import UserRegistrationForm, ResendActivationLinkForm


@pytest.mark.django_db
class TestResendActivationLinkForm:
    """
    Test of Resend Activation Link Form.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module
        for more information.
        """
        self.form = UserRegistrationForm()
        self.link_form = ResendActivationLinkForm()
        self.user = UserFactory()
        self.data = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'password': self.user.password,
            'confirm_password': self.user.password,
            'acct_type': 'IND',
            'toc': True,
        }

    def test_resend_link_form_is_not_bound(self):
        """
        Test if resend_link_form is not bound.
        """
        assert self.link_form.is_bound == False, 'Returns False if form is not bound.'

    def test_resend_link_form_is_bound(self):
        """
        Test if resend_link_form is bound.
        """
        self.link_form = ResendActivationLinkForm(data={})

        assert self.link_form.is_bound == True, 'Returns True if form is bound.'

    def test_resend_link_form_is_valid(self):
        "Test if ResendActivationLinkForm is valid."

        form = ResendActivationLinkForm(data={'email': 'testymctest@test.com'})

        assert form.is_valid() == True, 'Returns True if form is valid.'

    def test_resend_link_form_errors(self):
        """
        Test for form errors if not data provided.     
        """
        form = ResendActivationLinkForm(data={})

        assert 'This field is required.' in form[
            'email'].errors, 'Returns error if no data provided to form.'

    def test_resend_link_cleaned_data(self):
        """
        Test ResendActivationLinkForm data is cleaned.
        """
        form = ResendActivationLinkForm(data={'email': 'testymctest@test.com'})

        form.is_valid()

        assert 'testymctest@test.com' in form.cleaned_data.get(
            'email'), 'Returns cleaned_data from email.'

    def test_resend_link_invalid_email(self):
        """
        Test for invalid email address.
        """
        form = ResendActivationLinkForm(data={'email': 'testymctest'})

        assert 'Enter a valid email address.' in form[
            'email'].errors, 'returns invalid email address error.'
