from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import Profile, User, UserFaceImage
from election.models import ElectionForm


class InlineElectionForm(admin.StackedInline):
    model = ElectionForm

    fieldsets = (
        (None, {'fields': ('voter', )}),
        (None, {'fields': ('father_name', 'mother_name', 'dob', 'gender',
                           'citizenship_issued_district',
                           'citizenship')}),
        (None, {
         'fields': (('province', 'district'), ('muncipality', 'ward'), 'tole')}),
    )
    radio_fields = {'gender': admin.HORIZONTAL}


class InlineFaceImage(admin.StackedInline):
    model = UserFaceImage


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    inlines = [InlineFaceImage, InlineElectionForm]
    fieldsets = (
        (None, {'fields': ('citizenship_number', 'email', 'password')}),
        (_('Personal info'), {'fields': (('first_name', 'middle_name'), 'last_name',
                                         'avatar',)}),
        (_('Permissions'), {'classes': ('extrapretty'),
                            'fields': (('is_active', 'is_staff'), 'is_superuser', 'is_form_filled',
                                       ('is_voter', 'is_candidate',
                                        'is_verified_candidate'),
                                       )}),
        (_('User permissions'), {'classes': ('collapse',),
                                 'fields': ('user_permissions', )}),
        (_('Important dates'), {'classes': ('collapse', 'extrapretty'),
                                'fields': ('last_login', 'date_joined')}),
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
                    'full_name', 'is_staff', 'is_form_filled', 'is_voter', 'is_candidate', 'is_verified_candidate',)
    list_display_links = ('citizenship_number', 'email',)
    search_fields = ('citizenship_number', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser',
                   'is_form_filled', 'is_voter', )
    ordering = ('citizenship_number',)

    def full_name(self, obj):
        return '{}'.format(obj.get_full_name)


class ProfileAdmin(admin.ModelAdmin):
    model = Profile

    list_display = ('user', 'full_name')

    def full_name(self, obj):
        return '{}'.format(obj.user.get_full_name)


admin.site.register(User, CustomUserAdmin)
# admin.site.register(UserFaceImage)
admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(Group)
