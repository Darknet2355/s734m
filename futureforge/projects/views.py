from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Project


def project_list(request):
    projects = Project.objects.filter(status='published').prefetch_related('technologies')

    category = request.GET.get('category')
    if category:
        projects = projects.filter(category=category)

    audience = request.GET.get('audience')
    if audience:
        projects = projects.filter(target_audience=audience)

    paginator = Paginator(projects, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'projects/list.html', {
        'page_obj': page_obj,
        'category_choices': Project.CATEGORY_CHOICES,
        'audience_choices': Project.AUDIENCE_CHOICES,
        'active_category': category,
        'active_audience': audience,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, status='published')
    related = Project.objects.filter(category=project.category, status='published').exclude(pk=project.pk)[:3]
    return render(request, 'projects/detail.html', {'project': project, 'related_projects': related})
