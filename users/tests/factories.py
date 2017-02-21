#!/usr/bin/env python
import factory

from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.hashers import make_password


from users.models import User, Profile
from users.models import create_user_profile

@factory.django.mute_signals(pre_save, post_save)
class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

	first_name = factory.Sequence(lambda n: 'Testy{0}'.format(n))
	last_name = factory.Sequence(lambda n: 'McTesty{0}'.format(n))
	username = factory.LazyAttribute(lambda n: '{0}{1}'.format(n.first_name, n.last_name[:3]))
	email = factory.LazyAttribute(lambda n: '{0}@testing.com'.format(n.first_name))
	password = factory.Sequence(lambda n: 'testpassword{:04d}'.format(n))


class RandomUserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

	first_name = factory.Faker('first_name', locale='en_US')
	last_name = factory.Faker('last_name', locale='en_US')
	username = factory.LazyAttribute(lambda n: '{0}{1}'.format(n.first_name, n.last_name[:3]))
	email = factory.LazyAttribute(lambda n: '{0}@testing.com'.format(n.first_name))
	password = 'testpassword'



class UserProfileFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Profile

	user = factory.SubFactory(UserFactory)


def make_chain():
	with factory.django.mute_signals(pre_save, post_save):
		return UserProfileFactory()