#!/usr/bin/env python

import pytest
import factory
import factory.django

from users.tests.factories import UserFactory
from users.models import User
from users.forms import UserRegistrationForm

@pytest.mark.django_db
class TestUserRegisrationForm:
    """
    Test of User Registration Form.
    """
    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module
        for more information.
        """
        self.user = UserFactory()

    def test_user_registration_form_is_not_bound(self):
        """
        Test if form is bound by passed data.
        """
        form = UserRegistrationForm()
        assert form.is_bound == False, 'Returns False if form is not bound by data.(no values passed)'

    def test_user_registration_form_is_bound(self):
        """
        Test if form is bound by passed data.
        """
        form = UserRegistrationForm(data={})

        #As per Django documentation, the data={} will return True even if no kwargs passed.
        assert form.is_bound == True, 'Returns True if form is bound by data.'

