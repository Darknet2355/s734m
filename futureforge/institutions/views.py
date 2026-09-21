from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Institution


def institution_list(request):
    institutions = Institution.objects.filter(is_active_partner=True)

    type_filter = request.GET.get('type')
    if type_filter:
        institutions = institutions.filter(type=type_filter)

    paginator = Paginator(institutions, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'institutions/list.html', {
        'page_obj': page_obj,
        'type_choices': Institution.TYPE_CHOICES,
        'active_type': type_filter,
    })


def institution_detail(request, slug):
    institution = get_object_or_404(Institution, slug=slug)
    return render(request, 'institutions/detail.html', {'institution': institution})
