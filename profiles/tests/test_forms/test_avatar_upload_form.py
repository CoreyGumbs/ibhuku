#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from users.models import User
from profiles.models import Profile, ProfileAvatar
from profiles.forms import AvatarUploadForm
from profiles.tests.factories import UserFactory


@pytest.mark.django_db
class TestAvatarUploadForm:
    """
    Test of the Profile Avatar Upload form.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        ProfileAvatar.objects.create(
            profile_id=self.profile.id, avatar='name.jpg')
        self.avatar = ProfileAvatar.objects.select_related(
            'profile').get(profile_id=self.profile.id)
        self.form = AvatarUploadForm({})

    def test_avatar_update_is_bound_method(self):
        assert self.form.is_bound == True, 'Should return True if form is bound.'
        form = AvatarUploadForm()
        assert form.is_bound == False, 'Should return False if form is not bound.'

    def test_avatar_update_is_valid_method(self):
        assert self.form.is_valid == True, 'Should return True if form is valid. Check form data kwargs.'
        form = AvatarUploadForm({})
        assert form.is_valid == False, 'Should return False if form is not valid.'
