#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.conf import settings


from profiles.models import Profile, ProfileAvatar
from profiles.tests.factories import UserFactory


@pytest.mark.django_db
class TestProfileAvatarModel:
    """
    Test Profile Avatar Model.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module
        for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.avatar = ProfileAvatar.objects.create(
            profile_id=self.profile.id, avatar='{0}{1}'.format(settings.MEDIA_URL, 'testy.jpg'))

    def test_avatar_created(self):
        """
        Test Avatar Created
        """
        assert ProfileAvatar.objects.all().count(
        ) == 1, 'Returns avatar objects count. Should = 1'

    def test_avatar_data(self):
        """
        Test created avatar data.
        """
        assert self.avatar.profile.id == 2
        assert self.avatar.avatar == '/media/'
