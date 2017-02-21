#!/usr/bin/env python
import pytest

from users.models import User
from users.tests.factories import UserFactory

@pytest.mark.django_db
class TestIUserModel:

    def setup(self):
        self.ran_user = UserFactory()
        self.user1 =  UserFactory(first_name='Testy')

    def test_user_instance(self):
        users = User.objects.all()
        assert self.user1.first_name == 'Testy'
        assert len(users) == 2





