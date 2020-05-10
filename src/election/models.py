import os
import time

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext as _

from accounts.models import User, upload_storage
from base.settings import BASE_DIR
from election.choices import DISTRICT_CHOICES, GENDER_CHOICES, PROVINCE_CHOICES


def citizenship_location(instance, filename):
    """
    Rename image name to a timestamp and saves to uploads/citizenship_number/avatar/timestamp directory .
    """
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name, extension = os.path.splitext(filename)
    return os.path.join('uploads', str(instance.voter.citizenship_number), 'citizenship', timestr + extension)


class ElectionForm(models.Model):
    voter = models.OneToOneField(User, verbose_name=_(
        'citizenship number'), on_delete=models.CASCADE, related_name='voter')
    father_name = models.CharField(
        _('father\'s name'), max_length=30, blank=True)
    mother_name = models.CharField(
        _('mother\'s name'), max_length=30, blank=True)
    dob = models.DateField(_('date of birth'), blank=True, null=True)
    gender = models.CharField(_('gender'), blank=True,
                              max_length=15, choices=GENDER_CHOICES)
    citizenship_issued_district = models.CharField(
        _('citizenship issued district'), max_length=15, blank=True, choices=DISTRICT_CHOICES)

    citizenship = models.ImageField(
        _('Citizenship image'), upload_to=citizenship_location, storage=upload_storage, blank=True, help_text=_('Citizenship photo'))

    # Address Information
    province = models.CharField(
        _('province number'), max_length=15, blank=True, choices=PROVINCE_CHOICES)
    district = models.CharField(
        _('district'), max_length=15, blank=True, choices=DISTRICT_CHOICES)
    muncipality = models.CharField(_('muncipality'), max_length=30, blank=True)
    ward = models.IntegerField(_('ward number'), blank=True, null=True)
    tole = models.CharField(_('tole'), max_length=30, blank=True)

    # Dates
    date_submitted = models.DateTimeField(
        _('submission date'), blank=True, null=True, default=timezone.now)
    date_edited = models.DateTimeField(
        _('edit date'), blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name = _('election form')
        verbose_name_plural = _('election forms')

    def __str__(self):
        return str(self.voter.citizenship_number)


def save_election_form(sender, instance, **kwargs):
    instance.voter.is_form_filled = True
    instance.voter.save()


post_save.connect(save_election_form, sender=ElectionForm)
