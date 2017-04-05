#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.core.urlresolvers import reverse, resolve

from profiles.models import Profile
from profiles.forms import ProfileUpdateForm, UserUpdateForm
from profiles.tests.factories import UserFactory

from users.models import User
from profiles.models import Profile
from profiles.views import profile_dashboard, user_update


@pytest.mark.django_db
class TestUserUpdate:
    """
    Test User Update View.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.select_related(
            'user').get(user_id=self.user.id)

    def test_user_update_view(self, client):
        """
        Test user update view status.
        """
        response = client.get(
            reverse('profiles:update', kwargs={'pk': self.user.id, 'username': '-JohnDoe_1977'}))

        assert response.status_code == 200, 'Returns 200 if view status True.'
        assert response.resolver_match.url_name == 'update', 'Returns url name.'
        assert response.resolver_match.view_name == 'profiles:update', 'Returns view name.'

    def test_user_update_view_kwargs(self, client):
        """
        Test the passing of view/url kwargs.
        """
        response = client.get(reverse('profiles:update', kwargs={
                              'pk': self.user.id, 'username': self.user.username}))

        assert response.resolver_match.kwargs == {
            'pk': str(self.user.id), 'username': self.user.username}, 'Returns kwargs passed in url.'

    def test_user_view_rendering(self, client):
        """
        Test user_update view template context, content, and rendering.
        """
        response = client.get(reverse('profiles:update', kwargs={
                              'pk': self.user.id, 'username': self.user.username}))

        assert response.templates[
            0].name == 'profiles/user_update.html', 'Returns url/path of view template.'
        assert 'Ibhuku | Update Account' in response.content.decode(
            'utf8'), 'Returns True if title rendered in html.'
        assert 'form' in response.context, 'Returns True if form context is found.'
        assert '</form>' in response.content.decode(
            'utf8'), 'Returns True if html tag rendered in content.'
