#!/usr/bin/env python
import pytest
import factory
import factory.django

from users.models import User
from users.views import CreateUserAccountView


class TestCreateAccountView():
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
