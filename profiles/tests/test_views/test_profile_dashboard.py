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
class TestProfileDashboard:
    """
    Test of Profile Dashboard View.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)

    def test_profile_dashboard_view(self, client):
        """
        Test of profile dashboard view functionality.
        """
        response = client.get(
            reverse('profiles:dashboard', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.status_code == 200, 'Returns 200 if page found.'

    def test_profile_dashboard_view_name(self, client):
        """
        Test profile dashboard function name parameters. 
        """
        response = client.get(
            reverse('profiles:dashboard', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.resolver_match.func.__name__ == 'profile_dashboard', 'Returns the view function name.'
        assert response.resolver_match.view_name == 'profiles:dashboard', 'Returns view name.'
        assert response.resolver_match.url_name == 'dashboard', 'Returns url name.'

    def test_profile_dashboard_template_rendering(self, client):
        """
        Test of profile dashboard template and rendering.
        """
        response = client.get(
            reverse('profiles:dashboard', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.templates[0].name == 'profiles/profile_dashboard.html'
        assert 'Ibhuku | Profile' in response.content.decode('utf8')
        assert response.context['profile'] == self.profile

    def test_profile_dashboard_kwargs(self, client):
        """
        Test of profile dashboard url kwargs.
        """
        response = client.get(
            reverse('profiles:dashboard', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.resolver_match.kwargs == {
            'pk': '4', 'username': 'Testy3McT'}

    def test_profile_dashboard_retrieves_correct_user(self, client):
        response = client.get(
            reverse('profiles:dashboard', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.context[
            'profile'].user.first_name == self.user.first_name
