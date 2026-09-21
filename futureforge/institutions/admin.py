from django.contrib import admin

from .models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'is_active_partner')
    list_filter = ('type', 'is_active_partner')
    search_fields = ('name', 'location')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('programs_conducted',)
