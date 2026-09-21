from django.contrib import admin

from .models import SocialLink, TeamMember


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'order', 'is_active')
    list_filter = ('is_active', 'position')
    search_fields = ('full_name', 'position')
    prepopulated_fields = {'slug': ('full_name',)}
    inlines = [SocialLinkInline]
