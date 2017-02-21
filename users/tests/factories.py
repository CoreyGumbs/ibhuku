#!/usr/bin/env python
import factory

from django.contrib.auth.hashers import make_password


from users.models import User

class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

	first_name = factory.Faker('first_name', locale='en_US')
	last_name = factory.Faker('last_name', locale='en_US')
	username = factory.LazyAttribute(lambda n: '{0}{1}'.format(n.first_name, n.last_name[:3]))
	email = factory.LazyAttribute(lambda n: '{0}@testing.com'.format(n.first_name))
	password = make_password('testpassword')