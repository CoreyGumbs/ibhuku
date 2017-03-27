#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.core.urlresolvers import reverse, resolve

from profiles.models import Profile
from profiles.forms import ProfileUpdateForm
from profiles.tests.factories import UserFactory

from users.models import User
from profiles.models import Profile
from profiles.views import profile_dashboard


@pytest.mark.django_db
class TestProfileDashboard:
    """
    Test of Profile Dashboard View.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)

    def test_profile_dashboard_view(self, client):
        response = client.get(
            reverse('profiles:dashboard', kwargs={'pk': self.user.id}))
        assert response.status_code == 200
