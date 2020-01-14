# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth import (login as auth_login,
                                 update_session_auth_hash)
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import TemplateView

from users.forms import RegisterForm
from helpers.tokens import account_activation_token


class HomeView(TemplateView):
    template_name = "dashboard/home.html"


class UserSignup(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm

    # On successful form submission
    def get_success_url(self):
        return reverse('login')

    # Validate forms
    def form_valid(self, form):
        self.object = form.save()  # saves Father and Children
        mail_subject = 'Activate your account.'
        message = render_to_string('users/account_active_email.html', {
            'user': self.object,
            'domain': self.request.environ.get('HTTP_ORIGIN'),
            'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
            'token': account_activation_token.make_token(self.object),
        })
        to_email = form.cleaned_data.get('email')
        send_mail(
            mail_subject,
            message,
            'no-reply@example.com',
            [to_email],
            fail_silently=False,
        )
        messages.success(self.request, _(
            'Thank You for subscribing! Please activate your account.')
        )
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return super(UserSignup, self).form_invalid(form)


def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
