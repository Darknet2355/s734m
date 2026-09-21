from django.urls import path

from . import views

app_name = 'institutions'

urlpatterns = [
    path('', views.institution_list, name='institution_list'),
    path('<slug:slug>/', views.institution_detail, name='institution_detail'),
]
