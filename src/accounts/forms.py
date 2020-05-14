from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       ReadOnlyPasswordHashField)
from django.db.models import Q

from .models import User, UserFaceImage
from .utils import base64_file
from accounts.models import Profile
from PIL import Image


# Admin form
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('citizenship_number', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Admin form
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('citizenship_number', 'email', 'password', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# User signup form
class UserSignupForm(UserCreationForm):
    image = forms.CharField(widget=forms.HiddenInput)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('citizenship_number', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    # ========================================
    # We are inhereting UserCreationForm so we don't clean_password2 because it is already defined in UserCreationForm class.

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')

    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        # if not commit:
        #     raise NotImplementedError(
        #         "Can't create User and UserFaceImage without database save")

        user = super(UserSignupForm, self).save(commit=False)

        if commit:
            image = base64_file(self.data['image'])
            face_image = UserFaceImage(user=user, image=image)
            face_image.save()
            user.save()
        return user


# User login form
class UserLoginForm(forms.Form):
    image = forms.CharField(widget=forms.HiddenInput())
    citizenship_number = forms.IntegerField(label='Citizenship Number')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        citizenship_number = self.cleaned_data.get('citizenship_number')
        password = self.cleaned_data.get('password')

        user_qs = User.objects.filter(
            Q(citizenship_number=citizenship_number)).distinct()

        if not user_qs.exists() and user_qs.count() != 1:
            raise forms.ValidationError(
                "Invalid credentials - user does not exist")

        user_obj = user_qs.first()

        if not user_obj.check_password(password):
            raise forms.ValidationError("Password isn't correct!")

        return super(UserLoginForm, self).clean(*args, **kwargs)


# Authentication form
class AuthenticationForm(AuthenticationForm):
    image = forms.CharField(widget=forms.HiddenInput())

# Password change form


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def clean(self, *args, **kwargs):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords don't match")

        return super(PasswordChangeForm, self).clean(*args, **kwargs)


# Password reset request form
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')

        user_qs = User.objects.filter(email=email)

        if not user_qs.exists():
            raise forms.ValidationError(
                "User doesn't exist with provided email!")

        return super(PasswordResetRequestForm, self).clean(*args, **kwargs)


# class set password form
class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password not match!')
        return password2


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('avatar', 'x', 'y', 'width', 'height', )

    def save(self, commit=True):
        photo = super(PhotoForm, self).save(commit=False)

        if commit:
            photo = super(PhotoForm, self).save()
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            image = Image.open(photo.avatar)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(photo.avatar.path)

        return photo