#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string
import random

import pytest
import factory
import factory.django

from profiles.profilelib.strip_url import strip_url_name_punctuation
from profiles.models import Profile
from profiles.forms import ProfileUpdateForm
from profiles.tests.factories import UserFactory


@pytest.mark.django_db
class TestStripUrlName:
    """
    Test of strip_url_name_punctuation method.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.form = ProfileUpdateForm()
        self.current_occupation = 'Teacher'
        self.location = 'New York, N.Y.'

    def test_url_name_unauthorized_punctuation(self, client):
        unauthorized_punc = [x for x in string.punctuation]

        text = ' Testy_ McTesty%@  ' + \
            str(random.choice(unauthorized_punc)) + \
            str(random.choice(unauthorized_punc))

        url_name = ''.join(text.split())

        assert str(unauthorized_punc) not in strip_url_name_punctuation(
            url_name)

        assert 'Testy_McTesty' == strip_url_name_punctuation(url_name)
