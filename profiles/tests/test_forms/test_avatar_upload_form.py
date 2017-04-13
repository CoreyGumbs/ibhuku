#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import tempfile
import pytest
import factory
import factory.django
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile

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
        self.avatar = ProfileAvatar.objects.select_related(
            'profile').get(profile_id=self.profile.id)

        self.image = SimpleUploadedFile(name='test.jpg', content=open(
            'profiles/tests/test_images/test.jpg', 'rb').read())

        self.file_data = {
            'avatar': self.image,
        }
        self.data = {
            'profile_id': self.profile.id,
            'avatar': self.image,
        }

        self.form = AvatarUploadForm(self.data, self.file_data)

    def test_avatar_upload_is_bound_method(self):
        """
        Test form's is_bound() method.
        """
        assert self.form.is_bound == True, 'Should return True if form is bound.'
        form = AvatarUploadForm()
        assert form.is_bound == False, 'Should return False if form is not bound.'

    def test_avatar_upload_is_valid_method(self):
        """
        Test form's is_valid() method.
        """
        assert self.form.is_valid(
        ) == True, 'Should return True if form is valid. Check form data kwargs.'
        form = AvatarUploadForm()
        assert form.is_valid() == False, 'Should return False if form is not valid.'

    def test_avatar_upload_clean_method(self):
        """
        Test avatar upload field clean method.
        """
        self.form.is_valid()
        assert self.form.clean_avatar(
        ).name == 'test.jpg', 'Should return name of uploaded image file.'

    def test_avatar_upload_form_errors(self):
        """
        Test form errors.
        """
        image = SimpleUploadedFile(name='test.gif', content=open(
            'profiles/tests/test_images/test.gif', 'rb').read())

        file_data = {'avatar': image}

        data = {'profile_id': self.profile.id, 'avatar': image}

        form = AvatarUploadForm(data, file_data)

        assert form.has_error(
            'avatar', code='wrong_file_format') == True, 'Should return True if form has error on field.'
        assert form.errors == {'avatar': [
            'Unsupported file format. Please upload JPG or PNG file.']}, 'Returns field error message.'
