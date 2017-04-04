#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string
import random

import pytest
import factory
import factory.django

from profiles.profilelib.strip_url import strip_punctuation


@pytest.mark.django_db
class TestStripUrlName:
    """
    Test of strip_punctuation method.
    """

    def test_url_name_unauthorized_punctuation(self, client):
        """
        test url_name input to strip_url_name_punctuation method.
        Test will fail/False if the authorized punctuation in method is called.
        """
        # selects random punctuation characters from string.punctuation and
        # adds them to string.
        text = ' Testy_ McTesty%@  ' + \
            str(random.choice(string.punctuation)) + \
            str(random.choice(string.punctuation))

        # removes whitespace
        url_name = ''.join(text.split())

        assert text not in strip_punctuation(
            url_name), 'Should return newly created string without unauthorized punctuation'

        assert 'Testy_McTesty' == strip_punctuation(
            url_name), 'Should return data from method call without whitespace and wrong punctuation.'
