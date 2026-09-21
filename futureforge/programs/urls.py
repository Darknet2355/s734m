from django.urls import path

from . import views

app_name = 'programs'

urlpatterns = [
    path('', views.program_list, name='program_list'),
    path('<slug:slug>/', views.program_detail, name='program_detail'),
]
