from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy

from users.forms import UserRegistrationForm
# Create your views here.


def CreateUserAccountView(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
	else:
		form = UserRegistrationForm()

	context = {
		'form': form,
	}
	return render(request, 'users/registration.html', context)
