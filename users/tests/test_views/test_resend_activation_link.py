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
from users.models import User
from users.views import resend_activation_link


@pytest.mark.django_db
class TestResendActivationLinkView:

    def setup(self):
        self.user = UserFactory()

    def test_resend_activation_link_view(self, client):
        response = client.get('/accounts/reset/')
        assert response.status_code == 200
        assert response.resolver_match.url_name == 'activation-reset'
        assert response.resolver_match.func.__name__ == 'resend_activation_link'

    def test_resend_activation_view_template_context_html_rendering(self, client):
        response = client.get('/accounts/reset/')
        assert response.templates[
            0].name == 'users/resend_activation_link.html'
        assert 'form' in response.context
        assert 'Ibhuku | Resend Link' in response.content.decode('utf8')

    def test_resend_activation_link_new_email(self, client):
        response = client.post(
            '/accounts/reset/', {'email': self.user.email}, follow=True)

        assert response.status_code == 200
        assert 'Ibhuku | Activation Link Emailed' in response.content.decode(
            'utf8')
        assert response.templates[
            0].name == 'users/account_activation_sent.html', 'Should return rendered template path.'
        assert len(
            mail.outbox) == 1, 'Returns 1 mailbox entry if confirm account email sent.'
        assert mail.outbox[
            0].subject == 'Welcome to Ibhuku.com. Confirm your email.'
        assert mail.outbox[0].to == ['Testy2@testing.com']
        assert 'By clicking on the following button/link, you are confirming your email address' in str(mail.outbox[
            0].body)

    def test_resend_activation_link_new_email_account_confirmed(self, client):
        # set user.is_active = True
        self.user.is_active = True
        self.user.save()

        response = client.post(
            '/accounts/reset/', {'email': self.user.email}, follow=True)

        assert response.resolver_match.url_name == 'activation-exists'
        assert 'Ibhuku | Account Exists' in response.content.decode(
            'utf8')
        assert response.status_code == 200
        assert len(
            mail.outbox) == 0, 'Returns 1 mailbox entry if confirm account email sent.'
