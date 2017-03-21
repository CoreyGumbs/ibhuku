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
        assert 'Resend Link' in response.content.decode('utf8')
