#!/usr/bin/env python
import pytest
import factory
import factory.django

from users.models import User
from users.views import CreateUserAccountView

class TestCreateAccountView():

    def test_accounts_index_redirects_to_registration_view(self, client):
        response = client.get('/accounts/', follow=True)
        assert response.resolver_match.url_name == 'register'
        assert response.status_code == 200
        #assert response.resolver_match.func.__name__ == 'CreateUserAccountView'
