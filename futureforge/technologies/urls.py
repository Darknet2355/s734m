from django.urls import path

from . import views

app_name = 'technologies'

urlpatterns = [
    path('', views.technology_list, name='technology_list'),
    path('<slug:slug>/', views.technology_detail, name='technology_detail'),
]
