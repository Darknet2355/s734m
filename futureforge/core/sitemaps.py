from django.contrib.sitemaps import Sitemap

from blog.models import BlogPost
from programs.models import Program
from projects.models import Project
from services.models import Service
from technologies.models import Technology


class ProgramSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Program.objects.filter(status='active')

    def location(self, obj):
        return obj.get_absolute_url()


class TechnologySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Technology.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Project.objects.filter(status='published')

    def location(self, obj):
        return obj.get_absolute_url()


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()


class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(status='published')

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    'programs': ProgramSitemap,
    'technologies': TechnologySitemap,
    'projects': ProjectSitemap,
    'services': ServiceSitemap,
    'blog': BlogPostSitemap,
}
