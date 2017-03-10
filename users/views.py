from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy

from users.forms import UserRegistrationForm
# Create your views here.


def CreateUserAccountView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.password = make_password(
                form.cleaned_data['password'])
            new_user.save()
            try:
                user = User.objects.get(email__exact=form.instance.email)
            except:
                pass
            return HttpResponse('Welcome')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'users/registration.html', context)


def ConfirmAccountEmailActivationLink(request, uidb64=None, token=None, token_generator=default_token_generator):
    return HttpResponse('Hi.')
