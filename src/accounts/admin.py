from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import User, UserFaceImage


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('citizenship_number', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_voter',
                                       'is_candidate', 'is_verified_candidate',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # Used for creating user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('citizenship_number', 'email', 'password1', 'password2')}
         ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('citizenship_number', 'email',
                    'first_name', 'last_name', 'is_staff')
    list_display_links = ('citizenship_number', 'email',)
    search_fields = ('citizenship_number', 'email', 'first_name', 'last_name')
    ordering = ('citizenship_number',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserFaceImage)
admin.site.unregister(Group)
