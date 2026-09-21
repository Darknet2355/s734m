from django.core.paginator import Paginator
from django.shortcuts import render

from .models import MediaItem


def media_list(request):
    items = MediaItem.objects.filter(is_published=True)

    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)

    media_type = request.GET.get('type')
    if media_type:
        items = items.filter(media_type=media_type)

    paginator = Paginator(items, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'media/list.html', {
        'page_obj': page_obj,
        'category_choices': MediaItem.CATEGORY_CHOICES,
        'type_choices': MediaItem.TYPE_CHOICES,
        'active_category': category,
        'active_type': media_type,
    })
