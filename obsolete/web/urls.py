"""
URL configuration for the web project.

This module defines the URL patterns for the web application.
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home),
    path("sign-in/", auth_views.LoginView.as_view(template_name="sign_in.html")),
    path("sign-out/", auth_views.LogoutView.as_view(next_page="/")),
]
