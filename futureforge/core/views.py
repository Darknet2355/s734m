from itertools import chain

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from blog.models import BlogPost
from institutions.models import Institution
from programs.models import Program
from projects.models import Project
from services.models import Service
from team.models import TeamMember
from technologies.models import Technology

from .forms import SearchForm

# Static "empowering innovation" focus areas shown on the homepage.
FOCUS_AREAS = [
    {'icon': 'fa-solid fa-robot', 'title': 'Robotics', 'text': 'Design, build and program robots from the ground up.'},
    {'icon': 'fa-solid fa-brain', 'title': 'Artificial Intelligence', 'text': 'Hands-on AI and machine learning for real problems.'},
    {'icon': 'fa-solid fa-code', 'title': 'Coding', 'text': 'Programming fundamentals through to advanced software skills.'},
    {'icon': 'fa-solid fa-microchip', 'title': 'Electronics', 'text': 'Circuits, sensors and components learners can touch and test.'},
    {'icon': 'fa-solid fa-wifi', 'title': 'IoT', 'text': 'Connected devices that sense, decide and act in the real world.'},
    {'icon': 'fa-solid fa-server', 'title': 'Embedded Systems', 'text': 'Microcontrollers powering real hardware projects.'},
]

WHY_FUTUREFORGE = [
    {'icon': 'fa-solid fa-hands-bubbles', 'title': 'Hands-On Learning', 'text': 'Learners build real, working projects — not just theory.'},
    {'icon': 'fa-solid fa-chalkboard-user', 'title': 'Experienced Trainers', 'text': 'Certified engineers and educators lead every session.'},
    {'icon': 'fa-solid fa-diagram-project', 'title': 'Real-World Projects', 'text': 'Every program ends with a tangible, working innovation.'},
    {'icon': 'fa-solid fa-lightbulb', 'title': 'Innovation-Focused', 'text': 'We teach learners to solve problems, not just follow steps.'},
    {'icon': 'fa-solid fa-handshake', 'title': 'Institutional Partnerships', 'text': 'Trusted by schools, universities and organizations.'},
    {'icon': 'fa-solid fa-screwdriver-wrench', 'title': 'Practical Tech Skills', 'text': 'Arduino, ESP32, Raspberry Pi, Python, AI and more.'},
]

HOW_WE_TEACH = [
    {'step': 1, 'title': 'Identify Learner Needs', 'text': 'We assess the audience, skill level and goals.'},
    {'step': 2, 'title': 'Introduce the Concept', 'text': 'Clear, simple explanations of the technology or idea.'},
    {'step': 3, 'title': 'Demonstrate the Technology', 'text': 'Trainers show the concept in action.'},
    {'step': 4, 'title': 'Hands-On Practical Training', 'text': 'Learners get hardware and code in their hands.'},
    {'step': 5, 'title': 'Build a Project', 'text': 'Learners apply the skill to a real, working build.'},
    {'step': 6, 'title': 'Test and Improve', 'text': 'Iteration, debugging and refinement.'},
    {'step': 7, 'title': 'Present the Innovation', 'text': 'Learners showcase what they built with confidence.'},
]


def home(request):
    context = {
        'stats': {
            'students_trained': 2500,
            'institutions_reached': Institution.objects.count() or 45,
            'projects_built': Project.objects.count() or 60,
            'training_programs': Program.objects.filter(status='active').count() or 20,
        },
        'focus_areas': FOCUS_AREAS,
        'why_futureforge': WHY_FUTUREFORGE,
        'featured_programs': Program.objects.filter(status='active', is_featured=True)[:3],
        'featured_projects': Project.objects.filter(status='published', is_featured=True)[:3],
        'latest_posts': BlogPost.objects.filter(status='published')[:3],
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html', {'how_we_teach': HOW_WE_TEACH})


def search(request):
    form = SearchForm(request.GET or None)
    query = request.GET.get('q', '').strip()
    results = {'programs': [], 'technologies': [], 'projects': [], 'services': [], 'posts': []}

    if query:
        results['programs'] = Program.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query), status='active'
        )
        results['technologies'] = Technology.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        results['projects'] = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query), status='published'
        )
        results['services'] = Service.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query), is_active=True
        )
        results['posts'] = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query),
            status='published'
        )

    total_results = sum(len(v) for v in results.values())

    return render(request, 'search_results.html', {
        'form': form, 'query': query, 'results': results, 'total_results': total_results,
    })


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /dashboard/",
        "Disallow: /accounts/",
        "Disallow: /django-admin/",
        "Allow: /",
        "",
        f"Sitemap: {settings.SITE_DOMAIN}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def error_404(request, exception=None):
    return render(request, '404.html', status=404)


def error_403(request, exception=None):
    return render(request, '403.html', status=403)


def error_500(request):
    return render(request, '500.html', status=500)


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /dashboard/",
        "Disallow: /accounts/",
        "Disallow: /django-admin/",
        "Allow: /",
        "",
        f"Sitemap: {settings.SITE_DOMAIN}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
