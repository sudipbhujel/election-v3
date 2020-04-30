from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User
from django.db.models import Q


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
class UserSignupForm(forms.ModelForm):
    email = forms.EmailField(max_length=200)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('citizenship_number', 'email', 'first_name',
                  'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
    
    def save(self, commit=True):
        user = super(UserSignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


# User login form
class UserLoginForm(forms.Form):
    citizenship_number = forms.IntegerField(label='Citizenship Number')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        citizenship_number = self.cleaned_data.get('citizenship_number')
        password = self.cleaned_data.get('password')

        user_qs = User.objects.filter(Q(citizenship_number__iexact=citizenship_number)).distinct()

        if not user_qs.exists() and user_qs.count() != 1:
            raise forms.ValidationError("Invalid credentials - user does not exist")

        user_obj = user_qs.first()

        if not user_obj.check_password(password):
            raise forms.ValidationError("Credentials are not correct")

        self.cleaned_data['user_obj'] = user_obj

        return super(UserLoginForm, self).clean(*args, **kwargs)
