#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from profiles.models import Profile
from profiles.forms import ProfileUpdateForm
from profiles.tests.factories import UserFactory


@pytest.mark.django_db
class TestUpdateProfileForm:
    """
    Test UpdateProfileForm
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.form = ProfileUpdateForm()
        self.bio_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean in augue a arcu aliquet laoreet nec sed purus. Nullam rhoncus massa sed enim faucibus, id venenatis felis pulvinar. Aliquam a tellus sagittis, pulvinar metus et, aliquam libero. Nunc id metus id dui varius vulputate. Ut sed tortor felis. In quis dignissim risus. Fusce bibendum ullamcorper est, ac rutrum enim. Cras ac urna convallis, fringilla tortor ut, mattis enim. In sodales mattis dolor, vel aliquet augue tempus sed. Mauris at augue quis tortor maximus faucibus. Sed molestie venenatis turpis molestie euismod. Pellentesque dictum sagittis erat eu facilisis'

    def test_profile_update_form_is_not_bound(self):
        """
        Test ProfileUpdateForm is bound.
        """
        assert self.form.is_bound == False, 'Returns False if form is not bound.'

    def test_profile_update_form_is_bound(self):
        """
        Test ProfileUpdateForm is bound
        """
        form = ProfileUpdateForm(data={})

        assert form.is_bound == True, 'Returns True if form is bound.'

    def test_profile_update_form_is_not_valid(self):
        """
        Test form.is_valid() method.
        """
        assert self.form.is_valid() == False

    def test_profile_update_form_is_valid(self):
        """
        Test form.is_valid() method.
        """
        form = ProfileUpdateForm(data={'bio': 'Test Text.'})
        assert form.is_valid() == True

    def test_profile_update_form_field_errors(self):
        """
        Test form field errors and validation.
        """
        form = ProfileUpdateForm(data={'bio': self.bio_text})
        assert form.has_error(
            'bio', code='profile_bio_long') == True, 'Returns True if form field has an error.'
        assert form.errors == {
            'bio': ['You have exceeded the maximum length of 140 characters.']}, 'Returns kwargs of form field and error where error is reported.'
