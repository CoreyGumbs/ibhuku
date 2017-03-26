#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import factory
import factory.django

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse, resolve
from django.template.loader import render_to_string

from users.tests.factories import UserFactory
from profiles.models import Profile
from users.models import User
from users.views import resend_activation_link


@pytest.mark.django_db
class TestResendActivationLinkView:
    """
    Test of resend_activation_link view.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module
        for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.create(user_id=self.user.id)

    def test_resend_activation_link_view(self, client):
        """
        Test the resend_activation_link view.
        """

        response = client.get('/accounts/reset/')
        assert response.status_code == 200
        assert response.resolver_match.url_name == 'activation-reset'
        assert response.resolver_match.func.__name__ == 'resend_activation_link'

    def test_resend_activation_view_template_context_html_rendering(self, client):
        """
        Test context and html of resend_activation_link view and template.
        """
        response = client.get('/accounts/reset/')

        assert response.templates[
            0].name == 'users/resend_activation_link.html', 'Should return correct path of view template.'
        assert 'form' in response.context, 'Should return "form" context from view.'
        assert 'Ibhuku | Resend Link' in response.content.decode(
            'utf8'), 'Returns correct page <title> found on page.'

    def test_resend_activation_link_new_email(self, client):
        """
        Test new activation link resent to user.
        """
        response = client.post(
            '/accounts/reset/', {'email': self.user.email}, follow=True)

        assert response.status_code == 200, 'Returns 200 if page redirection is True.'
        assert 'Ibhuku | Activation Link Emailed' in response.content.decode(
            'utf8'), 'Returns correct page <title> found on page.'
        assert response.templates[
            0].name == 'users/account_activation_sent.html', 'Should return rendered template path.'
        assert len(
            mail.outbox) == 1, 'Returns 1 mailbox entry if confirm account email sent.'
        assert mail.outbox[
            0].subject == 'Welcome to Ibhuku.com. Confirm your email.', 'Returns email subject.'
        assert mail.outbox[0].to == ['Testy16@testing.com']
        assert 'By clicking on the following button/link, you are confirming your email address' in str(mail.outbox[
            0].body), 'Should return email body text.'

    def test_resend_activation_link_new_email_account_confirmed(self, client):
        """
        Test resend activation link response if verified account/email is being used.
        """
        self.user.is_active = True
        self.user.save()

        response = client.post(
            '/accounts/reset/', {'email': self.user.email}, follow=True)

        assert response.resolver_match.url_name == 'activation-exists', 'Returns view url'
        assert 'Ibhuku | Account Exists' in response.content.decode(
            'utf8'), 'Returns correct page <title> found on page.'
        assert response.status_code == 200, 'Returns 200 if successful redirect'
        assert len(
            mail.outbox) == 1, 'Returns 1 mailbox entry if already confirmed email sent.'
        assert mail.outbox[
            0].subject == 'Your accounts is already confirmed.', 'Should return subject of email sent to user.'
        assert mail.outbox[0].to == [
            'Testy17@testing.com'], 'Should return email message was sent to.'
        assert 'Testy17@testing.com' in str(mail.outbox[
            0].body), 'Should return the user email address used to confirm the account in email text body.'
