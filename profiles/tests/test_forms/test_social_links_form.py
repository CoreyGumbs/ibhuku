#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.test import override_settings

from users.models import User
from profiles.models import Profile, ProfileAvatar
from profiles.forms import ProfileSocialMediaForm
from profiles.tests.factories import UserFactory


@pytest.mark.django_db
class TestSocialLinksForm:
    """
    Test Social Links Form
    """
    @override_settings(MEDIA_ROOT='/tmp/django_test/')
    def setup(self):
        """
        Set up test data fixtures.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.avatar = ProfileAvatar.objects.select_related(
            'profile').get(profile_id=self.profile.id)
        self.data = {
            'facebook': 'http://www.facebook.com',
            'twitter': 'http://www.twitter.com',
            'google': 'http://www.google.com',
        }

    def test_social_media_form_is_bound_method(self, client):
        """
        Test form  .is_bound() method.
        """
        bound_form = ProfileSocialMediaForm(self.data)
        unbound_form = ProfileSocialMediaForm()
        assert bound_form.is_bound == True, 'Returns True if form is bound by data.'
        assert unbound_form.is_bound == False, 'Returns False if form is unbound by data'

    def test_social_media_form_is_valid_method(self, client):
        """
        Test form data is valid.
        """
        pass
