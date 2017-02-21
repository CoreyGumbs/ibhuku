#!/usr/bin/env python
import pytest

from users.models import User
from users.tests.factories import UserFactory, RandomUserFactory

@pytest.mark.django_db
class TestIUserModel:

    def setup(self):
       self.user1 = UserFactory()
       self.user2 = UserFactory(first_name='John', last_name='', email='DoeBoy123@testing.com', )
       self.users = User.objects.all()

    def test_user_instance_created(self):
        assert self.user1.first_name == 'Testy'
        assert self.user1.email == 'Testy@testing.com'
        assert self.user1.password == 'testpassword'

    def test_multiple_users_created(self):
        assert len(self.users) == 2

    def test_user_instance_get_full_name_method(self):
        assert self.user1.get_full_name() == 'TMcTesty'

    def test_user_no_last_name_get_full_name_method(self):
        assert self.user2.get_full_name() == 'John'
       





