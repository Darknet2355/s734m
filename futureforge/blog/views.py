from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import BlogCategory, BlogPost


def post_list(request):
    posts = BlogPost.objects.filter(status='published').select_related('category', 'author')
    categories = BlogCategory.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    query = request.GET.get('q', '').strip()
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query)
        )

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'blog/list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'active_category': category_slug,
        'query': query,
    })


def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    related_posts = BlogPost.objects.filter(
        category=post.category, status='published'
    ).exclude(pk=post.pk)[:3]
    return render(request, 'blog/detail.html', {'post': post, 'related_posts': related_posts})
