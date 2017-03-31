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
        assert self.profile.user.first_name == 'Testy1', 'Should  return associated user first name.'

    def test_profile_unicode_method(self):
        """
        Test the __unicode__ method of model.
        """
        assert self.profile.__unicode__() == 'Testy2McT', 'Should return username.'

    def test_profile_str_method(self):
        """
        Test the __str__ method of model.
        """
        assert self.profile.__str__() == 'Testy3McT', 'Should return username.'

    def test_profile_bio_field_saves(self):
        """
        Test the bio model field saves data.
        """
        assert self.profile.bio == '', 'Should return original bio field data.'

        self.profile.bio = 'This is a test.'
        self.profile.save()

        assert self.profile.bio == 'This is a test.', 'Should return newly saved data to bio field.'

    def test_profile_location_field_saves(self):
        """
        Test location model field.
        """
        assert self.profile.location == '', 'Should return original location field data.'

        self.profile.location = 'Queens, N.Y.'
        self.profile.save()

        assert self.profile.location == 'Queens, N.Y.', 'Should return newly saved data to location field.'

    def test_profile_email_confirmed_field_saves(self):
        """
        Test email_confirmed model field.
        """
        assert self.profile.email_confirmed == False, 'Should return default value of False.'

        self.profile.email_confirmed = True
        self.profile.save()

        assert self.profile.email_confirmed == True, 'Should return value of True.'

    def test_profile_user_reverse_relations(self):
        assert self.profile.user.get_full_name(
        ) == 'Testy7 McTesty7', 'Should return full name from User model method.'

    def test_profile_url_name_saves(self):
        """
        Test url_name field.
        """
        assert self.profile.url_name == '', 'Should return blank.'

        self.profile.url_name = 'yippiman'
        self.profile.save()

        assert self.profile.url_name == 'yippiman', 'Should return newly saved data'

    def test_user_url_name_method(self):
        """
        Test profile user_url_name method.
        """
        self.profile.url_name = self.user.username
        self.profile.save()
        assert self.profile.user_url_name() == '@Testy9McT'
