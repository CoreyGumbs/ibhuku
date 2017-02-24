#!/usr/bin/env python
import pytest
import factory
import factory.django

from django.test import TestCase

from users.models import User
from users.views import CreateUserAccountView


class TestCreateAccountView:
    """
    Test of CreateUserAccountView
    """

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
        assert response.templates[0].name == 'users/registration.html'

    def test_create_user_account_view_template_content(self, client):
        """
        Test CreateUserAccountView template.
        """
        response = client.get('/accounts/register/')
        assert '<title>Ibhuku | Register</title>' in response.content.decode('utf8')