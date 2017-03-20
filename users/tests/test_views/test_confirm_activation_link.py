#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import factory
import factory.django

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.tests.factories import UserFactory
from users.models import User
from users.views import confirm_activation_link


@pytest.mark.django_db
class TestAccountActivationLink:
    """
    Test to emailed account activation link.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module
        for more information.
        """
        self.user = UserFactory()
        self.user_uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.user_token = default_token_generator.make_token(self.user)

    def test_confirm_account_link_view(self, client):
        """
        """
        response = client.post(reverse('users:activate', kwargs={
            'uidb64': self.user_uid, 'token': self.user_token}))
        assert response.status_code == 200
        assert response.resolver_match.func.__name__ == 'confirm_activation_link'
        assert response.templates[
            0].name == 'users/activation_link.html', 'Should return rendered template path.'
