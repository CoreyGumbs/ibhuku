#!/usr/bin/env python

import pytest
import factory
import factory.django

from users.tests.factories import UserFactory
from users.models import User
from users.forms import UserRegistrationForm


@pytest.mark.django_db
