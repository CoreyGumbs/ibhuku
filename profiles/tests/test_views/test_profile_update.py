#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.core.urlresolvers import reverse, resolve

from profiles.models import Profile
from profiles.forms import ProfileUpdateForm
from profiles.tests.factories import UserFactory

from users.models import User
from profiles.models import Profile
from profiles.views import profile_dashboard


@pytest.mark.django_db
class TestProfileUpdateView:
    """
    Test of the Profile Update view.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.select_related(
            'user').get(user_id=self.user.id)

    def test_profile_update_view_page_status(self, client):
        response = client.get(
            reverse('profiles:update', kwargs={'pk': self.user.id}))

        assert response.status_code == 200
        assert response.resolver_match.url_name == 'update'
        assert response.resolver_match.view_name == 'profiles:update'

    def test_profile_update_kwargs(self, client):
        """
        Test of profile_update kwarg(s).
        """
        response = client.get(
            reverse('profiles:update', kwargs={'pk': self.user.id}))

        assert response.resolver_match.kwargs == {'pk': str(self.user.id)}

    def test_profile_update_view_rendering(self, client):
        """
        Test profile_update view template context, content, and rendering.
        """
        response = client.get(
            reverse('profiles:update', kwargs={'pk': self.user.id}))
        assert response.templates[0].name == 'profiles/profile_update.html'
        assert 'Ibhuku | Update Profile' in response.content.decode('utf8')
        assert 'form' in response.context
