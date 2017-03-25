#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.db.models.signals import post_save

import factory
from faker import Faker


from users.models import User
from profiles.models import Profile


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    first_name = factory.Sequence(lambda n: 'Testy{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'McTesty{0}'.format(n))
    username = factory.LazyAttribute(
        lambda n: '{0}{1}'.format(n.first_name, n.last_name[:3]))
    email = factory.LazyAttribute(
        lambda n: '{0}@testing.com'.format(n.first_name))
    password = factory.Sequence(lambda n: 'testpassword{:04d}'.format(n))


# @factory.django.mute_signals(post_save)
# class ProfileFactory(factory.django.DjangoModelFactory):

#     class Meta:
#         model = Profile

#     user = factory.SubFactory(UserFactory)


# def make_chain():
#     with factory.django.mute_signals(post_save):
#         return UserProfileFactory()
