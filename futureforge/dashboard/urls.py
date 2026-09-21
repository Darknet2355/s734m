from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.global_search, name='global_search'),

    # Programs
    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/add/', views.ProgramCreateView.as_view(), name='program_add'),
    path('programs/<int:pk>/edit/', views.ProgramUpdateView.as_view(), name='program_edit'),
    path('programs/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),

    # Technologies
    path('technologies/', views.TechnologyListView.as_view(), name='technology_list'),
    path('technologies/add/', views.TechnologyCreateView.as_view(), name='technology_add'),
    path('technologies/<int:pk>/edit/', views.TechnologyUpdateView.as_view(), name='technology_edit'),
    path('technologies/<int:pk>/delete/', views.TechnologyDeleteView.as_view(), name='technology_delete'),

    # Institutions
    path('institutions/', views.InstitutionListView.as_view(), name='institution_list'),
    path('institutions/add/', views.InstitutionCreateView.as_view(), name='institution_add'),
    path('institutions/<int:pk>/edit/', views.InstitutionUpdateView.as_view(), name='institution_edit'),
    path('institutions/<int:pk>/delete/', views.InstitutionDeleteView.as_view(), name='institution_delete'),

    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/add/', views.ProjectCreateView.as_view(), name='project_add'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),

    # Services
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/add/', views.ServiceCreateView.as_view(), name='service_add'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

    # Team
    path('team/', views.TeamListView.as_view(), name='team_list'),
    path('team/add/', views.TeamCreateView.as_view(), name='team_add'),
    path('team/<int:pk>/edit/', views.TeamUpdateView.as_view(), name='team_edit'),
    path('team/<int:pk>/delete/', views.TeamDeleteView.as_view(), name='team_delete'),

    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/add/', views.BlogCreateView.as_view(), name='blog_add'),
    path('blog/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='blog_edit'),
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/<int:pk>/toggle-publish/', views.blog_toggle_publish, name='blog_toggle_publish'),

    # Media
    path('media/', views.MediaListView.as_view(), name='media_list'),
    path('media/add/', views.MediaCreateView.as_view(), name='media_add'),
    path('media/<int:pk>/edit/', views.MediaUpdateView.as_view(), name='media_edit'),
    path('media/<int:pk>/delete/', views.MediaDeleteView.as_view(), name='media_delete'),

    # Messages
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/toggle-read/', views.message_toggle_read, name='message_toggle_read'),
    path('messages/<int:pk>/delete/', views.message_delete, name='message_delete'),

    # Training Requests
    path('training-requests/', views.training_request_list, name='training_request_list'),
    path('training-requests/<int:pk>/update-status/', views.training_request_update_status, name='training_request_update_status'),
    path('training-requests/<int:pk>/delete/', views.training_request_delete, name='training_request_delete'),
]
