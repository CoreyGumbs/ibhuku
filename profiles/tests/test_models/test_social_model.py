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
    Test the social media profile links model.
    '''

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.social = ProfileSocial.objects.select_related(
            'profile').get(profile_id=self.profile.id)

    def test_model_exists(self):
        '''
        Test ProfileSocial model exists.
        '''
        assert self.social._meta.db_table == 'profile_social_links', 'Should return the db_table name Meta on model.'
        assert ProfileSocial.objects.count(
        ) == 1, 'Should return correct count of objects created.'
        assert self.social.profile_id == self.profile.id, 'Should return profile_id.'

    def test_model_unicode_method(self):
        '''
        Test __unicode__ method.
        '''
        assert self.social.__unicode__() == 'Testy1McT', 'Returns __unicode__ string from model.'

    def test_model_str_method(self):
        '''
        Test __str__ method.
        '''
        assert self.social.__str__() == 'Testy2McT', 'Returns __str__ string from model.'

    def test_model_saves_new_data(self):
        self.social.facebook = 'http://www.facebook.com'
        self.social.save()
        assert self.social.facebook == 'facebook.com'
