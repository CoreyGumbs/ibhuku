#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.core.urlresolvers import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User
from profiles.models import Profile, ProfileAvatar
from profiles.forms import AvatarUploadForm
from profiles.tests.factories import UserFactory
from profiles.views import profile_dashboard, user_update


@pytest.mark.django_db
class TestAvatarUpload:
    """
    Test avatar upload view.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.avatar = ProfileAvatar.objects.select_related(
            'profile').get(profile_id=self.profile.id)

    def test_avatar_upload_view(self, client):
        """
        Test Avatar Upload View.
        """
        response = client.get(reverse(
            'profiles:av-upload', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.status_code == 302, 'Returns 302 on page redirect'
        assert response.resolver_match.url_name == 'av-upload'
        assert response.resolver_match.view_name == 'profiles:av-upload'

    def test_avatar_upload_parameter_kwargs(self, client):
        """
        Test avatar upload kwargs.
        """
        response = client.get(reverse(
            'profiles:av-upload', kwargs={'pk': self.user.id, 'username': self.profile.user.username}))
        assert response.resolver_match.kwargs == {
            'pk': '2', 'username': 'Testy1McT'}
