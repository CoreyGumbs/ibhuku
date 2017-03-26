#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from profiles.models import Profile
from profiles.tests.factories import UserFactory


@pytest.mark.django_db
class TestProfileModel:
    """
    Test of the Profile model.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module
        for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)

    def test_user_created(self):
        """
        Test to see if user was created.
        """
        assert self.user.first_name == 'Testy0', 'Should return user first_name.'
        assert self.user.id == 1, 'Should return user pk/id'

    def test_user_profile_created(self):
        """
        Test if user profile created.
        """
        assert self.profile.user.first_name == 'Testy1', 'Should '

    def test_profile_unicode_method(self):
        """
        Test the __unicode__ method of model.
        """
        assert self.profile.__unicode__() == 'Testy2McT'

    def test_profile_str_method(self):
        """
        Test the __str__ method of model.
        """
        assert self.profile.__str__() == 'Testy3McT'

    def test_profile_bio_saves(self):
        """
        Test the bio model field saves data.
        """
        assert self.profile.bio == ''

        self.profile.bio = 'This is a test.'
        self.profile.save()

        assert self.profile.bio == 'This is a test.'
