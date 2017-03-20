from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse, resolve
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse_lazy

from users.userslib.confirm_email import confirm_account_link

from users.forms import UserRegistrationForm
from users.models import User
# Create your views here.


def create_user_acccount(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.password = make_password(
                form.cleaned_data['password'])
            new_user.username = form.instance.generic_username()
            new_user.save()
            try:
                user = User.objects.get(email__exact=form.instance.email)
                token = default_token_generator.make_token(user)
                if user:
                    confirm_account_link(
                        user, form.instance.email, token, request=request)
                    return HttpResponseRedirect(reverse('users:activation-sent'))
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse('users:error'))
            return HttpResponseRedirect(reverse('users:activation-sent'))
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'users/registration.html', context)


def user_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')


def confirm_activation_link(request, uidb64=None, token=None, token_generator=default_token_generator):
    try:
        user = User.objects.get(
            pk=force_text(urlsafe_base64_decode(uidb64)))
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        user.is_active = True
        user.save()
    else:
        validlink = False

    context = {
        'validlink': validlink,
    }

    return render(request, 'users/activation_link.html', context)


def resend_activation_link(request):
    return HttpResponse('test')
