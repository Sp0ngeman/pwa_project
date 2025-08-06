"""
Main URL Configuration for ChipIn Project
=========================================

URL routing for the ChipIn secure social media platform.
Routes requests to appropriate apps and views.
"""

from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from chipin import views as chipin_views
from .views import serve_service_worker

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # App URLs
    path('users/', include(("users.urls", "users"), namespace="users")),
    path('chipin/', include(("chipin.urls", "chipin"), namespace="chipin")),
    
    # Authentication (django-allauth)
    path('accounts/', include('allauth.urls')),
    
    # Home page - redirect to chipin dashboard
    path('', chipin_views.index, name='home'),
    
    # Service worker for PWA functionality
    path('service-worker.js', serve_service_worker, name='service_worker'),
]
