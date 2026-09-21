from django.contrib import admin
from django.utils.html import format_html

from .models import Program, ProgramCategory


@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty_level', 'status', 'is_featured', 'image_preview')
    list_filter = ('category', 'difficulty_level', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'
