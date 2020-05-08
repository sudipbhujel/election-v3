from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from accounts.authenticate import FaceIdAuthBackend
from accounts.forms import (AuthenticationForm, PasswordChangeForm,
                            UserLoginForm, UserSignupForm)
from accounts.models import User
from accounts.tokens import account_activation_token
from accounts.utils import prepare_image


@login_required
def home(request):
    context = {}
    return render(request, 'accounts/home.html', context)


class SignupView(View):
    form_class = UserSignupForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'You are already logged in!')
            return redirect('accounts:home')
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            form.save()
            current_site = get_current_site(request)

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
            citizenship_number = form.cleaned_data['citizenship_number']
            password = form.cleaned_data['password']
            face_image = prepare_image(form.cleaned_data['image'])

            face_id = FaceIdAuthBackend()
            user = face_id.authenticate(
                citizenship_number=citizenship_number, password=password, face_id=face_image)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are successfully logged in!')
                return redirect('accounts:home')
            else:
                form.add_error(
                    None, "Your face didn't match.")
        context = {'form': form}
        return render(request, self.template_name, context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out successfully!')
    return redirect('accounts:login')


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        
        if form.is_valid():
            form.save()
            print(form)
            messages.success(request, 'You have changed your password...')
            return redirect('accounts:home')
    
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}

    return render(request, 'accounts/password_change.html', context)

# class PasswordChangeView(View):
#     form_class = PasswordChangeForm
#     template_name = 'accounts/password_change.html'

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(user=request.user)
#         context = {'form': form}
#         return render(request, self.template_name, context)
    
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(data=request.POST, user=request.user)
        
#         if form.is_valid():
#             messages.success(request, 'You have Changed Your Password...')
#             return redirect('home')
#         context = {'form': form}
#         return render(request, self.template_name, context)