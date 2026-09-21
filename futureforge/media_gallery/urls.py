from django.urls import path

from . import views

app_name = 'media_gallery'

urlpatterns = [
    path('', views.media_list, name='media_list'),
]
