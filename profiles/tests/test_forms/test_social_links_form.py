#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.test import override_settings

from users.models import User
from profiles.models import Profile, ProfileAvatar, ProfileSocial
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
        self.social_media = ProfileSocial.objects.select_related(
            'profile').get(profile_id=self.profile.id)
        self.data = {
            'facebook': 'http://www.facebook.com',
            'twitter': 'http://www.twitter.com',
            'google': 'http://www.google.com',
            'linkedin': 'http://www.linkedin.com',
            'instagram': 'http://www.instagram.com',
            'pintrest': 'http://www.pintrest.com',
            'website': 'http://www.coreygumbs.com',
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
        valid_form = ProfileSocialMediaForm(self.data)
        assert valid_form.is_valid() == True, "Returns True if form data valid."

    def test_social_media_form_values(self, client):
        """
        Test form passes data.
        """
        form = ProfileSocialMediaForm(
            data=self.data)
        assert form['facebook'].value(
        ) == 'http://www.facebook.com', 'Returns value of data passed to form.'
        assert form['website'].value(
        ) == 'http://www.coreygumbs.com', 'Returns value of data passed to form.'

    def test_social_media_form_errors(self, client):
        """
        Test form errors.
        """
        form = ProfileSocialMediaForm(
            data={'facebook': 'facebook'})
        assert form.has_error(
            'facebook') == True, 'Should return True if there is an error'
        assert form.errors == {'facebook': [
            'Enter a valid URL.']}, 'Should return field error message'

    def test_social_media_form_clean_method(self, client):
        """
        Test clean method.
        """
        form = ProfileSocialMediaForm(
            data=self.data)
        form.is_valid()
        assert form.clean() == {
            'facebook': 'http://www.facebook.com',
            'twitter': 'http://www.twitter.com',
            'google': 'http://www.google.com',
            'linkedin': 'http://www.linkedin.com',
            'instagram': 'http://www.instagram.com',
            'pintrest': 'http://www.pintrest.com',
            'website': 'http://www.coreygumbs.com',
        }, 'Returns cleaned data dict.'
