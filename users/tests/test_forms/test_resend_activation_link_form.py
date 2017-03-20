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

    def test_resend_link_form_is_bound(self):
        assert self.link_form.is_bound == False
