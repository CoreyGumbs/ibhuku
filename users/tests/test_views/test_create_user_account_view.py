#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import factory
import factory.django

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse, resolve

from users.tests.factories import UserFactory
from users.models import User
from users.views import create_user_acccount


@pytest.mark.django_db
class TestCreateAccountView:
    """
    Test of create_user_acccount view.
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
        """
        Test user was created.
        """
        user = User.objects.get(email__exact=self.user.email)
        assert len(User.objects.all()
                   ) == 1, 'Returns number of users created/found in database.'
        assert user.email == 'Testy0@testing.com', 'Should return user email.'
        assert user.username == 'Testy0McT', 'Should return saved generically generated username.'

    def test_accounts_index_redirects_to_registration_view(self, client):
        """
        Test that the accounts index directory
        and url: '/accounts/' redirects to '/accounts/register/'.
        """
        response = client.get('/accounts/', follow=True)
        assert response.resolver_match.url_name == 'register', 'Should return redirected url name.'
        assert response.status_code == 200, 'Should return 200 on redirect.'
        assert response.templates[
            0].name == 'users/registration.html', 'Should return rendered template path.'

    def test_create_user_account_view_and_url(self, client):
        """
        Test CreateUserAccountView.
        """
        response = client.get('/accounts/register/')
        assert response.status_code == 200, 'Should return 200.'
        assert response.resolver_match.func.__name__ == 'create_user_acccount', 'Should return correct name of view.'

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
        assert 'form' in response.context, 'Should return "form" context parameter.'

    def test_account_confirmation_email_sent_view(self, client):
        """
        Test account created succes redirect and confirm account email sent.
        """
        response = client.post('/accounts/register/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@test.com',
            'password': self.user.password,
            'confirm_password': self.user.password,
            'acct_type': 'IND',
            'toc': True,
        }, follow=True)

        html = response.content.decode('utf-8')

        assert response.status_code == 200, 'Returns 200 if successful page redirection after POST.'
        assert response.templates[
            0].name == 'users/account_activation_sent.html', 'Should return rendered template path.'
        assert 'Activation Link Emailed' in html, 'Should return text found in page title.'
        assert len(
            mail.outbox) == 1, 'Returns 1 mailbox entry if confirm account email sent.'

    def test_account_creation_user_doesnt_exist(self):
        """"
        Test User.DoesNotExist exception
        """
        with pytest.raises(Exception) as excinfo:
            User.objects.get(email__exact="no_user@test.com")
        assert 'User matching query does not exist.' in str(excinfo.value)
