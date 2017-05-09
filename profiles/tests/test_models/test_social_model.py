#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.conf import settings

from users.models import User
from profiles.models import Profile, ProfileAvatar, ProfileSocial
from profiles.tests.factories import UserFactory


@pytest.mark.django_db
class TestSocialProfilesModel:
    '''
    Test the social media profile links page.
    '''

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.social = ProfileAvatar.objects.select_related(
            'profile').get(profile_id=self.profile.id)

    def test_model_exists(self):
        '''
        Test ProfileSocial model exists.
        '''
        assert ProfileSocial.objects.count(
        ) == 1, 'Should return correct count of objects created.'
