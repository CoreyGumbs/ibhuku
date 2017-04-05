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
            'pk': '2', 'username': 'Testy1McT'}
