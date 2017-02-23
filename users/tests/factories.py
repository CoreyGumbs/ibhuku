#!/usr/bin/env python
import factory
from faker import Faker

from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.hashers import make_password


from users.models import User, Profile
from users.models import create_user_profile

#produces 'fake' data that is consistent 
#every time test is run.
#Test will fail when new names added to test class.
#Just update new names to test and should pass.
fake = Faker()
fake.seed(4321)

@factory.django.mute_signals(pre_save, post_save)
class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

	first_name = factory.LazyAttribute(lambda n: fake.first_name())
	last_name = factory.LazyAttribute(lambda n: fake.last_name())
	username = factory.LazyAttribute(lambda n: '{0}{1}'.format(n.first_name, n.last_name[:3]))
	email = factory.LazyAttribute(lambda n: '{0}@testing.com'.format(n.first_name))
	password = factory.LazyAttribute(lambda n: '{0}'.format(fake.password()))


class UserProfileFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Profile

	user = factory.SubFactory(UserFactory)
	bio = factory.LazyAttribute(lambda n: fake.text(max_nb_chars=50))

	@factory.sequence
	def gender(n):
		if n % 2 == 0:
			return 'M'
		elif n % 2 == 1:
			return 'F'

	@factory.sequence
	def degree(n):
	 	if n % 2 == 0:
	 		return 'BD'
	 	elif n % 2 == 1:
	 		return 'MD'


def make_chain():
	with factory.django.mute_signals(pre_save, post_save):
		return UserProfileFactory()