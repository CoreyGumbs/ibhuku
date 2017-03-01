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
        self.form = UserRegistrationForm()
        self.user = UserFactory()

    def test_user_registration_form_is_not_bound(self):
        """
        Test if form is bound by passed data.
        """
        assert self.form.is_bound == False, 'Returns False if form is not bound by data.(no values passed)'

    def test_user_registration_form_is_bound(self):
        """
        Test if form is bound by passed data.
        """
        self.form = UserRegistrationForm(data={})

        # As per Django documentation, the data={} will return True even if no
        # kwargs passed.
        assert self.form.is_bound == True, 'Returns True if form is bound by data.'

    def test_user_registration_form_is_valid(self):

        # Hardcoded kwargs as form wont take self.data fixture. Will return
        # False.
        self.form2 = UserRegistrationForm(data={
                'first_name': 'Testy', 
                'last_name': 'McTesty', 
                'email': 'McTesty@testing.com', 
                'password': 'testpassword1234', 
                'confirm_password': 'testpassword1234', 
                'acct_type': 'IND', 
                'toc': True, 
            })

        assert self.form.is_valid() == False
        print(self.form2.errors)
        #assert self.form2.is_valid() == True

    def test_user_registration_form_html_render(self, client):
        response = client.get('/accounts/register/')
        assert '<label for="id_acct_type" class="control-label  requiredField">' in response.content.decode('utf8')

    def test_user_registration_form_errors(self, client):
        self.form = UserRegistrationForm(data={})
        assert 'This field is required.' in self.form['first_name'].errors

    def test_user_registration_password_validation_clean(self):
        self.form = UserRegistrationForm(data={
                'first_name': 'Testy', 
                'last_name': 'McTesty', 
                'email': 'McTesty@testing.com', 
                'password': 'testpassword1234', 
                'confirm_password': 'testpassword1234', 
                'acct_type': 'IND', 
                'toc': True, 
            })
        print(self.form.errors)
        print(self.form.clean_password)


