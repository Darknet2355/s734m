from django.urls import path

from . import views

app_name = 'inquiries'

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('request-training/', views.training_request_view, name='training_request'),
]
