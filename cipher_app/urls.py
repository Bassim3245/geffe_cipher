from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cipher/', views.cipher, name='cipher'),
    path('process_text/', views.process_text, name='process_text'),
]
