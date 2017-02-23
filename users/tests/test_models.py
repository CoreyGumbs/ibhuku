#!/usr/bin/env python
import pytest
import factory
import factory.django

from django.db.models.signals import pre_save, post_save

from users.models import User, Profile
from users.tests.factories import UserFactory, UserProfileFactory

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
        self.user2 = UserFactory(first_name='John', last_name='', email='DoeBoy123@testing.com')
        self.users = User.objects.all()

    #Test of User Model created instances
    def test_user1_instance_created(self):
        """
        Test for creation of a user instance in the database.
        """
        assert self.user1.first_name == 'Jonathan', 'Should return user first name.'
        assert self.user1.email == 'Jonathan@testing.com', 'Should return user email.'
        assert self.user1.password == '@2U&oPeldh', 'Should return user password.'

    def test_multiple_users_saved_in_database(self):
        """
        Test for number of user instances created in database.
        """
        assert len(self.users) == 2, 'Should return number of instances created in database'

    def test_user_instance_get_full_name_method(self):
        """
        Test the user model's get_full_name() method.
        """
        assert self.user1.get_full_name() == 'RKirk', 'Should return formatted name if last name provided by user.'
        assert self.user2.get_full_name() == 'John', 'Should return first name if no last name provided by user.'

    def test_user_get_short_name_method(self):
        """
        Test the user model's get_short_name() method.
        """
        assert self.user1.get_short_name() == 'VMorales', 'Should return formatted name if last name provided by user.'
        assert self.user2.get_short_name() ==  'John', 'Should return first name if no last name provided by user.'

    def test_user_model_saves(self):
        """
        Test user model saves/updates user changed/new data.
        """
        self.user1.password = 'testpassword12345'
        self.user1.is_active = True
        self.user1.save()
        assert self.user1.password == 'testpassword12345'
        assert self.user1.is_active == True

    #Test of User Model methods
    def test_user_model_unicode_method(self):
        """
        Test the user model's __unicode__() method.
        """
        assert self.user1.__unicode__() == 'TJackson', 'Should return formatted name if last name provided by user.'
        assert self.user2.__unicode__() == 'John', 'Should return first name if no last name provided by user.'

    def test_user_model_str_method(self):
        """
        Test the user model's __str__() method.
        """
        assert self.user1.__str__() == 'FDavis', 'Should return formatted name if last name provided by user.'
        assert self.user2.__str__() == 'John', 'Should return first name if no last name provided by user.'



@pytest.mark.django_db
class TestProfileModel:
    """
    Test Profile Model.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module
        for more info.
        """
        self.profile = UserProfileFactory()
        self.profile2 = UserProfileFactory()
        self.users = Profile.objects.all()

    #Test of Profile Model created instances
    def test_user_profile_instance_saved_in_database(self):
        """
        Test profile instances created in database.
        """
        assert len(self.users) == 2, 'Should return count of profiles created by user instance.'

    def test_user_profile_instance_created(self):
        """
        Test user foreign key reverse relation.
        """
        assert self.profile.user.get_full_name() == 'KGeorge', 'Should call get_full_name method from user model.'
        assert self.profile2.user.get_full_name() == 'PLopez', 'Should call get_full_name method from user model.'

    def test_user_profile_gender_field(self):
        """
        Test user profile gender choice field selection.
        """ 
        assert self.profile.gender == 'M', 'Should select M gender from choices.'
        assert self.profile2.gender == 'F', 'Should select F gender from choices.'

    def test_user_profile_degree_field(self):
        """
        Test user profile degree choice field selection.
        """
        assert self.profile.degree == 'BD'
        assert self.profile2.degree == 'MD'

    def test_user_profile_bio_field(self):
        assert self.profile.bio == 'Voluptates ex soluta itaque aperiam.'
        assert self.profile2.bio == 'Consequuntur esse ad sequi est.'


    #Test of Profile Model methods
    def test_user_profile_model_unicode_method(self):
        """
        Test profile __unicode__() method returns user instance.
        """
        assert self.profile.__unicode__() == 'SCollins', 'Should return user get_full_name method.'

    def test_user_profile_model_str_method(self):
        """
        Test profile __str__() method returns user instance.
        """
        assert self.profile.__str__()  == 'TShields', 'Should return user get_full_name method.'





