#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import factory
import factory.django

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
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
        Test confirm_activation_link view.
        """
        response = client.post(reverse('users:activate', kwargs={
            'uidb64': self.user_uid, 'token': self.user_token}))
        assert response.status_code == 200
        assert response.resolver_match.func.__name__ == 'confirm_activation_link'
        assert response.templates[
            0].name == 'users/activation_link.html', 'Should return rendered template path.'

    def test_confirm_activation_link_view_template_renders(self, client):
        response = client.get(reverse('users:activate', kwargs={
            'uidb64': self.user_uid, 'token': self.user_token}))
        html = response.content.decode('utf8')
        assert 'Ibhuku | Account Confirmed' in response.content.decode('utf8')

    def test_confirm_activation_link_uid64_parameter_invalid(self, client):
        response = client.get(reverse('users:activate', kwargs={
            'uidb64': b'MPB', 'token': self.user_token}))
        assert response.context['validlink'] == False

    def test_confirm_activation_link_token_parameter_invalid(self, client):
        response = client.get(reverse('users:activate', kwargs={
            'uidb64': self.user_uid, 'token': '12-2345A'}))
        assert response.context['validlink'] == False
        assert 'Link Expired' in response.content.decode('utf8')

    def test_confirm_activation_link_parameters_valid(self, client):
        response = client.get(reverse('users:activate', kwargs={
            'uidb64': self.user_uid, 'token': self.user_token}))
        assert response.context['validlink'] == True
        assert 'Account Confirmed' in response.content.decode('utf8')

    def test_confirm_activation_link_view_user_active(self, client):
        response = client.get(reverse('users:activate', kwargs={
            'uidb64': self.user_uid, 'token': self.user_token}))
        user = User.objects.get(email__exact=self.user.email)
        assert user.is_active == True
