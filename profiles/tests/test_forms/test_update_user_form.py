#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from profiles.models import Profile
from profiles.forms import ProfileUpdateForm, UserUpdateForm
from profiles.tests.factories import UserFactory
from users.models import User


@pytest.mark.django_db
class TestUpdateUserAccount:
    """
    Test of User Update Form.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.form = ProfileUpdateForm()
        self.user_update = UserUpdateForm()

    def test_user_update_form_bound(self):
        """
        Test user update form is_bound method.
        """
        assert self.user_update.is_bound == False, 'Returns False if form is not bound.'

        form = UserUpdateForm({})
        assert form.is_bound == True, 'Returns True if form bound.'

    def test_user_update_form_is_valid(self):
        """
        Test user update form is_valid() method.
        """
        assert self.user_update.is_valid() == False, 'Should return False if form is not valid.'

        form = UserUpdateForm(data={'first_name': 'Testy', 'last_name': 'McTesty',
                                    'email': 'testy@gmail.com', 'username': 'TestyMcTest13'})

        assert form.is_valid() == True, 'Returns True if form valid.'

    def test_user_update_form_values(self):
        """
        Test passing of forms values.
        """
        form = UserUpdateForm(data={'first_name': self.user.first_name, 'last_name': self.user.last_name,
                                    'email': 'testy@gmail.com', 'username': self.user.username})
        assert form['first_name'].value() == 'Testy2'
        assert form['username'].value() == self.user.username

    def test_user_update_form_field_errors(self):
        """
        Test of user update form field errors.
        """
        form = UserUpdateForm(data={'first_name': 'Testy', 'last_name': 'McTesty',
                                    'email': 'testy@gmail.com', 'username': 'TestyMcTest13@1!drterterter'})

        assert form.has_error('username') == True
        assert form.errors == {'username': [
            'The maximum length of characters is 15.']}
