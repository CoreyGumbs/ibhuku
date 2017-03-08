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

from users.userslib.confirm_email import confirm_account_link
from users.models import User


@pytest.mark.django_db
class TestConfirmAccountLink:

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
        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        assert mail.subject == 'Welcome to Ibhuku.com. Confirm your email.'
