from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from .models import User
from .tokens import account_activation_token
from .forms import UserSignupForm
from django.contrib import messages
from django.template.loader import render_to_string
from email.message import EmailMessage
from accounts.forms import UserLoginForm


def home(request):
    return HttpResponse('Worked!')


class SignupView(View):
    form_class = UserSignupForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            # mail_subject = 'Activate your blog account.'
            # message = render_to_string('acc_active_email.html', {
            #     'user': user,
            #     'protocol': 'http',
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email]
            # )
            # email.send()

            subject = 'Activate your Account'
            message = message = render_to_string('acc_active_email.html', {
                'user': user,
                'protocol': 'http',
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            user.email_user(subject, message)

            return HttpResponse('Please confirm your email address to complete the registration')
        context = {'form': form}
        return render(request, self.template_name, context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account is activated successfully!')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, request.FILES or None)

        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            messages.success(request, 'You are logged in successfully!')
            return redirect('home')
        context = {'form': form}
        return render(request, self.template_name, context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out successfully!')
    return redirect('login')
