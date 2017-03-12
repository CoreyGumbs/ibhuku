#!/usr/bin/env python

import pytest
import factory
import factory.django

from django.core import mail
from django.core.urlresolvers import reverse, resolve

from users.tests.factories import UserFactory
from users.models import User
from users.views import CreateUserAccountView


@pytest.mark.django_db
class TestCreateAccountView:
    """
    Test of CreateUserAccountView
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module
        for more information.
        """
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

    def test_user_exist(self):
        user = User.objects.get(email__exact=self.user.email)
        assert len(User.objects.all()) == 1
        assert user.email == 'Testy0@testing.com'

    def test_accounts_index_redirects_to_registration_view(self, client):
        """
        Test that the accounts index directory
        and url: '/accounts/' redirects to '/accounts/register/'.
        """
        response = client.get('/accounts/', follow=True)
        assert response.resolver_match.url_name == 'register', 'Should return redirected url name.'
        assert response.status_code == 200, 'Should return 200 on redirect.'

    def test_create_user_account_view_and_url(self, client):
        """
        Test CreateUserAccountView.
        """
        response = client.get('/accounts/register/')
        assert response.status_code == 200, 'Should return 200.'
        assert response.resolver_match.func.__name__ == 'CreateUserAccountView', 'Should return name of view.'

    def test_create_user_account_view_template(self, client):
        response = client.get('/accounts/register/')
        assert response.templates[
            0].name == 'users/registration.html', 'Should return rendered template path.'

    def test_create_user_account_view_template_content(self, client):
        """
        Test CreateUserAccountView template.
        """
        response = client.get('/accounts/register/')
        assert 'Ibhuku | Register' in response.content.decode(
            'utf8'), 'Should return current title data.'

    def test_create_user_account_view_template_context(self, client):
        """
        Test template context rendering.
        """
        response = client.get('/accounts/register/')
        assert 'form' in response.context

    def test_create_user_account_email_sent(self, client):
        response = client.post('/accounts/register/', {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'password': self.user.password,
            'confirm_password': self.user.password,
            'acct_type': 'IND',
            'toc': True,
        }, follow=True)
