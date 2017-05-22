#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.test import override_settings
from django.core.urlresolvers import reverse, resolve

from users.models import User
from profiles.models import Profile, ProfileAvatar, ProfileSocial
from profiles.forms import ProfileSocialMediaForm
from profiles.tests.factories import UserFactory
from profiles.views import social_media_links


@pytest.mark.django_db
class TestProfileSocialLinksView:
    """
    Test of social_media_links view.
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

    def test_social_media_links_view(self, client):
        """
        Test if social_media_links view exists.
        """
        response = client.get(reverse('profiles:socials', kwargs={
                              'pk': self.user.id, 'username': self.user.username}))

        assert response.status_code == 200, 'Returns 200 if there is an http response from view/url'
        assert response.resolver_match.url_name == 'socials'
        assert response.resolver_match.view_name == 'profiles:socials'
