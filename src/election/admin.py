from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from election.models import ElectionForm


class ElectionFormAdmin(admin.ModelAdmin):
    date_hierarchy = ('date_submitted')
    readonly_fields = ('date_submitted', 'date_edited', )
    fieldsets = (
        (None, {'fields': ('voter', )}),
        (_('Personal info'), {'fields': ('father_name', 'mother_name', 'dob', 'gender',
                                         'citizenship_issued_district',
                                         'citizenship')}),
        (_('Address info'), {
         'fields': (('province', 'district'), ('muncipality', 'ward'), 'tole')}),
        (_('Dates'),{'fields': ('date_submitted', 'date_edited'),}),
    )
    radio_fields = {'gender': admin.HORIZONTAL}

    list_display = ('voter', 'full_name', 'province', 'district',)
    list_display_links = ('voter', 'full_name', )
    search_fields = ('voter', )
    list_filter = ('gender', 'province', )
    ordering = ('voter', )

    def full_name(self, obj):
        return '{}'.format(obj.voter.get_full_name)


admin.site.register(ElectionForm, ElectionFormAdmin)
