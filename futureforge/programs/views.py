from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Program, ProgramCategory


def program_list(request):
    programs = Program.objects.filter(status='active').select_related('category')
    categories = ProgramCategory.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        programs = programs.filter(category__slug=category_slug)

    difficulty = request.GET.get('level')
    if difficulty:
        programs = programs.filter(difficulty_level=difficulty)

    paginator = Paginator(programs, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'programs/list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'active_category': category_slug,
        'active_level': difficulty,
        'difficulty_choices': Program.DIFFICULTY_CHOICES,
    })


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug, status='active')
    related = Program.objects.filter(category=program.category, status='active').exclude(pk=program.pk)[:3]
    return render(request, 'programs/detail.html', {'program': program, 'related_programs': related})
