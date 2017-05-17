#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from users.models import User
from profiles.models import Profile, ProfileAvatar
from profiles.forms import ProfileSocialMediaForm
from profiles.tests.factories import UserFactory


@pytest.mark.django_db
class TestSocialLinksForm:
    """
    Test Social Links Form
    """

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

    def test_social_media_links_form_is_bound(self, client):
        """
        Test form  .is_bound() method.
        """
        form = ProfileSocialMediaForm(self.data)
        assert form.is_bound == True, 'Returns True if form is bound by data.'
