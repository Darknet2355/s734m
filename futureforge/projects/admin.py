from django.contrib import admin
from django.utils.html import format_html

from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'target_audience', 'status', 'project_date', 'image_preview')
    list_filter = ('category', 'target_audience', 'status')
    search_fields = ('title', 'description')
    filter_horizontal = ('technologies',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.featured_image.url)
        return '-'
    image_preview.short_description = 'Preview'
