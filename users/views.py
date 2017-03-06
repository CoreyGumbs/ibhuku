from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy

from users.forms import UserRegistrationForm
# Create your views here.


def CreateUserAccountView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        print(form.instance.first_name)
        if form.is_valid():
            return HttpResponse('it works')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'users/registration.html', context)
