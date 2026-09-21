from django.contrib import admin

from .models import MediaItem


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'category', 'is_published')
    list_filter = ('media_type', 'category', 'is_published')
    search_fields = ('title', 'description')
