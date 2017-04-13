#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.core.urlresolvers import reverse, resolve

from users.models import User
from profiles.models import Profile, ProfileAvatar
from profiles.forms import AvatarUploadForm
from profiles.tests.factories import UserFactory
#from profiles.views import profile_dashboard, user_update


@pytest.mark.django_db
class TestAvatarUpload:
    """
    Test avatar upload view.
    """
