from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import TechCategory, Technology


def technology_list(request):
    technologies = Technology.objects.select_related('category').all()
    categories = TechCategory.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        technologies = technologies.filter(category__slug=category_slug)

    difficulty = request.GET.get('level')
    if difficulty:
        technologies = technologies.filter(difficulty=difficulty)

    paginator = Paginator(technologies, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'technologies/list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'active_category': category_slug,
        'active_level': difficulty,
        'difficulty_choices': Technology.DIFFICULTY_CHOICES,
    })


def technology_detail(request, slug):
    technology = get_object_or_404(Technology, slug=slug)
    related = Technology.objects.filter(category=technology.category).exclude(pk=technology.pk)[:4]
    related_projects = technology.projects.filter(status='published')[:3]
    return render(request, 'technologies/detail.html', {
        'technology': technology, 'related_technologies': related, 'related_projects': related_projects,
    })
