#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.conf import settings
from django.test import override_settings, modify_settings
from django.core.urlresolvers import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User
from profiles.models import Profile, ProfileAvatar
from profiles.forms import AvatarUploadForm
from profiles.tests.factories import UserFactory
from profiles.views import profile_dashboard, user_update


@pytest.mark.django_db
class TestAvatarUploadPageImageUpload:
    '''
    Test of profile avatar upload.
    Create generic/ directory in tmp directory and add test image. 
    Test will fail with out a tmp/django_test/generic/test_image.jpg directory.
    '''
    @override_settings(MEDIA_ROOT='/tmp/django_test/')
    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.avatar = ProfileAvatar.objects.select_related(
            'profile').get(profile_id=self.profile.id)

    @override_settings(MEDIA_ROOT='/tmp/django_test/')
    def test_avatar_upload_view(self, client):
        """
        Test Avatar Upload View.
        """
        image = SimpleUploadedFile(name='test.jpg', content=open(
            'profiles/tests/test_images/test.jpg', 'rb').read())

        response = client.post(reverse('profiles:av-upload', kwargs={
            'pk': self.user.id, 'username': self.user.username}), {'avatar': image})

        avatar = ProfileAvatar.objects.select_related(
            'profile').get(profile_id=self.user.id)

        assert response.status_code == 302, 'Returns 302'
        assert response.resolver_match.url_name == 'av-upload'
        assert response.resolver_match.view_name == 'profiles:av-upload'
        assert response.resolver_match.kwargs == {
            'pk': '1', 'username': 'Testy0McT'}
        assert avatar.avatar.name == 'user_1_profile/avatar/profile_Testy0McT.jpg', 'Should return new filename and path.'

    @override_settings(MEDIA_ROOT='/tmp/django_test/')
    def test_avatar_upload_parameter_kwargs(self, client):
        """
        Test avatar upload kwargs.
        """
        response = client.get(reverse(
            'profiles:av-upload', kwargs={'pk': self.user.id, 'username': self.profile.user.username}))
        assert response.resolver_match.kwargs == {
            'pk': '2', 'username': 'Testy1McT'}

    @override_settings(MEDIA_ROOT='/tmp/django_test/')
    def test_avatar_upload_image_saves(self, client):
        """
        Test of profile image upload saves to model.
        """
        image = SimpleUploadedFile(name='test.jpg', content=open(
            'profiles/tests/test_images/test.jpg', 'rb').read())

        response = client.post(reverse('profiles:av-upload', kwargs={
                               'pk': self.user.id, 'username': self.user.username}), {'avatar': image}, follow=True)

        avatar = ProfileAvatar.objects.select_related(
            'profile').get(profile_id=self.user.id)
        assert '/tmp/django_test/user_3_profile/avatar/' in avatar.avatar.path, 'Should return path of uploaded file.'
        assert avatar.avatar.name == 'user_3_profile/avatar/profile_Testy2McT.jpg', 'Should returnnew filename and path.'
