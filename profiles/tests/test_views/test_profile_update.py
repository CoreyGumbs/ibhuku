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
        """
        Test profile update view status.
        """
        response = client.get(
            reverse('profiles:edit', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.status_code == 200
        assert response.resolver_match.url_name == 'edit'
        assert response.resolver_match.view_name == 'profiles:edit'

    def test_profile_update_kwargs(self, client):
        """
        Test of profile_update kwarg(s).
        """
        response = client.get(
            reverse('profiles:edit', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.resolver_match.kwargs == {
            'pk': str(self.user.id), 'username': self.user.username}

    def test_profile_update_view_rendering(self, client):
        """
        Test profile_update view template context, content, and rendering.
        """
        response = client.get(
            reverse('profiles:edit', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.templates[0].name == 'profiles/profile_update.html'
        assert 'Ibhuku | Update Profile' in response.content.decode('utf8')
        assert 'form' in response.context

    def test_profile_update_view_returns_correct_profile(self, client):
        """
        Test profile_update returns correct profile.
        """
        response = client.get(
            reverse('profiles:edit', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.context[
            'profile'].user.first_name == self.user.first_name
        assert response.context['profile'].location == ''
        assert response.context['profile'].url_name == ''

    def test_profile_update_POST_and_save(self, client):
        """
        Test profile update view request.POST and form save.
        """
        # initial response post of profile data.
        response = client.post(reverse('profiles:edit', kwargs={'pk': self.user.id, 'username': self.user.username}), {
                               'bio': 'Tsfsdfsddf', 'location': 'New York', 'url_name': '!Test@ McTest-77'})

        # search for current profile.
        my_profile = Profile.objects.select_related(
            'user').get(pk=self.user.id)

        # get request to retrieve newly saved data.
        response = client.get(reverse('profiles:edit', kwargs={
                              'pk': self.user.id, 'username': self.user.username}))

        assert response.context[
            'profile'].url_name == 'TestMcTest-77', 'Returns cleaned url_name parameter.'
        assert my_profile.url_name == response.context[
            'profile'].url_name, 'Returns saved url_name parameter.'
        assert response.context[
            'profile'].location == 'New York', 'Returns saved location parameter.'
