from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from core.sitemaps import sitemaps
from core import views as core_views

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('', include('core.urls', namespace='core')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('programs/', include('programs.urls', namespace='programs')),
    path('technologies/', include('technologies.urls', namespace='technologies')),
    path('institutions/', include('institutions.urls', namespace='institutions')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('services/', include('services.urls', namespace='services')),
    path('team/', include('team.urls', namespace='team')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('media-gallery/', include('media_gallery.urls', namespace='media_gallery')),
    path('contact/', include('inquiries.urls', namespace='inquiries')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', core_views.robots_txt, name='robots_txt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

handler404 = 'core.views.error_404'
handler403 = 'core.views.error_403'
handler500 = 'core.views.error_500'
