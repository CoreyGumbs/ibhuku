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
            profile_id=self.profile.id)

    def test_avatar_created(self):
        """
        Test Avatar Created
        """
        assert ProfileAvatar.objects.all().count(
        ) == 1, 'Returns avatar objects count. Should = 1'

    def test_avatar_created_data(self):
        """
        Test created avatar data.
        """
        assert self.avatar.profile.id == 2, 'Returns created avatar instance id #.'
        assert self.avatar.avatar == 'media/generic/default.jpg', 'Returns avatar default file path.'

    def test_avatar_unicode_method(self):
        """
        Test of __unicode__ method.
        """
        assert self.avatar.__unicode__(
        ) == 'media/generic/default.jpg', 'Returns unicode method data.'

    def test_avatar_unicode_method(self):
        """
        Test of __str__ method.
        """
        assert self.avatar.__str__() == 'media/generic/default.jpg', 'Returns str method data.'

    def test_avatar_model_saves(self):
        """
        Test if ProfileAvatar saves new data in ImageField.
        """
        self.avatar.avatar = '{0}{1}'.format(settings.MEDIA_URL, 'me.jpg')
        self.avatar.save()

        assert self.avatar.avatar == '/media/me.jpg', 'Should return new image path.'

    def test_avatar_reverse_relations(self):
        """
        Test the foreign key reverse relations of ProfileAvatar.
        """
        assert self.avatar.profile.email_confirmed == False, 'Returns False if email_confirmed of Profile model is False.'
        assert self.avatar.profile.user.last_name == 'McTesty4', 'Returns last_name field of User model.'
