from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy

# Create your views here.
def CreateUserAccountView(request):
	return render(request, 'users/registration.html', context={'test': 'test'})
