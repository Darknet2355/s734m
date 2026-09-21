from django.contrib import admin

from .models import ContactMessage, TrainingRequest


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'email', 'subject', 'message')


@admin.register(TrainingRequest)
class TrainingRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'organization', 'service', 'preferred_date', 'status', 'created_at')
    list_filter = ('status', 'training_level', 'service')
    search_fields = ('full_name', 'organization', 'email')
