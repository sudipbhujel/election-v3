from base.settings import BASE_DIR
import os
import time

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _


# Custom User Manager
class UserManager(BaseUserManager):

    def _create_user(self, citizenship_number, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(citizenship_number=citizenship_number,
                          email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, citizenship_number, email, password=None, **extra_fields):
        return self._create_user(citizenship_number, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, citizenship_number, email, password, **extra_fields):
        return self._create_user(citizenship_number, email, password, True, True,
                                 **extra_fields)


# Profile Image name
location = os.path.join(BASE_DIR, 'accounts')
upload_storage = FileSystemStorage(location=location, base_url='/accounts')

def pp_location(instance, filename):
    """
    Rename image name to a timestamp and saves to profiles/citizenship_number directory .
    """
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name, extension = os.path.splitext(filename)
    return os.path.join('uploads', str(instance.citizenship_number), 'avatar', timestr + extension)


# Custom User
class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Citizenship Number, Email and password are required. Other fields are optional.
    """
    citizenship_number = models.IntegerField(
        _('citizenship number'), unique=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    profile_image = models.ImageField(
        _('profile image'), upload_to=pp_location, storage=upload_storage, blank=True, help_text=_('Profile picture'))

    # Roles
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin'
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    # Custom roles
    is_voter = models.BooleanField(_('voter'), default=False,
                                   help_text=_('Designates whether the user can vote.'))
    is_candidate = models.BooleanField(_('candidate'), default=False,
                                       help_text=_(''))
    is_verified_candidate = models.BooleanField(_('verified candidate'), default=False,
                                                help_text=_(''))

    # Important dates
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'citizenship_number'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


# UserFaceImage
def face_location(instance, filename):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name, extension = os.path.splitext(filename)
    return os.path.join('uploads', str(instance.user.citizenship_number), 'face', timestr + extension)


class UserFaceImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        _('face image'), upload_to=face_location, storage=upload_storage, blank=False)

    def __str__(self):
        return str(self.user.citizenship_number)
