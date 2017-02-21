#!/usr/bin/env python
import pytest

from users.models import User
from users.tests.factories import UserFactory, RandomUserFactory


@pytest.mark.django_db
class TestUserModel:
    """
    Test for the Users Model.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module
        for more information.
        """
        self.user1 = UserFactory()
        self.user2 = UserFactory(first_name='John', last_name='', email='DoeBoy123@testing.com', )
        self.users = User.objects.all()

    def test_user1_instance_created(self):
        """
        Test for creation of a user instance in the database.
        """
        assert self.user1.first_name == 'Testy', 'Should return user first name.'
        assert self.user1.email == 'Testy@testing.com', 'Should return user email.'
        assert self.user1.password == 'testpassword', 'Should return user password.'

    def test_multiple_users_saveed_in_database(self):
        """
        Test for number of user instances created in database.
        """
        assert len(self.users) == 2, 'Should return number of instances created in database'

    def test_user_instance_get_full_name_method(self):
        """
        Test the user model's get_full_name() method.
        """
        assert self.user1.get_full_name() == 'TMcTesty', 'Should return formatted name if last name provided by user.'
        assert self.user2.get_full_name() == 'John', 'Should return first name if no last name provided by user.'

    def test_user_get_short_name_method(self):
        """
        Test the user model's get_short_name() method.
        """
        assert self.user1.get_short_name() == 'TMcTesty', 'Should return formatted name if last name provided by user.'
        assert self.user2.get_short_name() ==  'John', 'Should return first name if no last name provided by user.'

    def test_user_model_unicode_method(self):
        """
        Test the user model's __unicode__() method.
        """
        assert self.user1.__unicode__() == 'TMcTesty', 'Should return formatted name if last name provided by user.'
        assert self.user2.__unicode__() == 'John', 'Should return first name if no last name provided by user.'

    def test_user_model_str_method(self):
        """
        Test the user model's __str__() method.
        """
        assert self.user1.__str__() == 'TMcTesty', 'Should return formatted name if last name provided by user.'
        assert self.user2.__str__() == 'John', 'Should return first name if no last name provided by user.'

       





