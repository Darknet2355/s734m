from django.shortcuts import get_object_or_404, render

from .models import TeamMember


def team_list(request):
    members = TeamMember.objects.filter(is_active=True).prefetch_related('social_links')
    return render(request, 'team/list.html', {'members': members})


def team_detail(request, slug):
    member = get_object_or_404(TeamMember, slug=slug, is_active=True)
    return render(request, 'team/detail.html', {'member': member})
