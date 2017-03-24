#!/usr/bin/env python

import pytest
import factory
import factory.django

from django.core import mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, resolve

from users.tests.factories import UserFactory

from users.userslib.confirm_email import confirm_account_link, already_confirmed_account
from users.models import User


@pytest.mark.django_db
class TestConfirmAccountLink:
    """
    Test ConfrimAccountLink Function.
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

    def test_confirm_email_response(self, mailoutbox, client):
        """
        Test that simulates the confrim email account function.
        """
        response = client.get('/accounts/register/')
        current_site = get_current_site(response.wsgi_request)
        site_name = current_site.name
        domain = current_site.domain
        use_https = False
        token = default_token_generator.make_token(self.user)
        context = {
            'user': self.user,
            'token': token,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'protocol': 'https' if use_https else 'http',
            'domain': domain,
            'site_name': site_name,
        }
        subject, from_email, to_email = 'Welcome to Ibhuku.com. Confirm your email.', 'Ibhuku Team <noreply@ibhuku.com>', self.user.email
        text_content = render_to_string('emails/test_email.txt', context)
        html_content = render_to_string('emails/test_email.html', context)
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        assert len(mailoutbox) == 1, 'Returns 1 if email was sent.'
        mail = mailoutbox[0]
        assert mail.subject == 'Welcome to Ibhuku.com. Confirm your email.', 'Should return email subject line of sent email.'
        assert mail.from_email == 'Ibhuku Team <noreply@ibhuku.com>', 'Should return "from email" found in email.'
        assert list(mail.to) == [
            'Testy0@testing.com'], 'Should return confirm link email to.'

    def test_confirm_account_link_lib(self, mailoutbox, client):
        """
        Test of the actual confirm_account_link function from the userslib.
        """
        response = client.get('/acounts/register/')

        token = default_token_generator.make_token(self.user)
        mail = confirm_account_link(
            self.user, self.user.email, token, request=response.wsgi_request)

        assert len(mailoutbox) == 1, 'Returns 1 if email has been sent.'
        sent_mail = mailoutbox[0]
        assert sent_mail.subject == 'Welcome to Ibhuku.com. Confirm your email.', 'Should return email subject line of sent email.'
        assert sent_mail.from_email == 'Ibhuku Team <noreply@ibhuku.com>', 'Should return "from email" found in email.'
        assert list(sent_mail.to) == [
            'Testy1@testing.com'], 'Should return user email used to register.'


@pytest.mark.django_db
class TestAlreadyConfirmedAccount:
    """
    Test AlreadyConfirmedAccount Function.
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

    def test_already_confirmed_account_email_response(self, client):
        """
        Test already_confirmed_account email is sent on already verified account.
        """
        self.user.is_active = True
        self.user.save()

        response = client.post(
            '/accounts/reset/', {'email': self.user.email}, follow=True)

        assert len(mail.outbox) == 1, 'Returns 1 if email has been sent.'
        assert mail.outbox[
            0].subject == 'Your accounts is already confirmed.', 'Should return email subject line of sent email.'
        assert mail.outbox[0].to == [
            'Testy2@testing.com'], 'Should return user email used to register.'
        assert 'You have received this email because there was an attempt to reset the activation link for your account.' in str(mail.outbox[
            0].body), 'Returns template text found in the body of sent email.'
