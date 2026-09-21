from django.contrib import admin
from django.utils.html import format_html

from .models import Technology, TechCategory


@admin.register(TechCategory)
class TechCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'difficulty', 'is_featured', 'image_preview')
    list_filter = ('category', 'difficulty')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'
