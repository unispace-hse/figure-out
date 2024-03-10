"""
Core models
"""

from django.urls import path
from . import views

urlpatterns = [
    # post views
    path("", views.index, name="root"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("setup/1", views.setup_priority_service, name="priorityservice"),
    path("setup/2", views.setup_character, name="character"),
    path("setup/3", views.setup_experience, name="experience"),
    path("logout/", views.user_logout, name="logout"),
    path("today", views.EventCreateView.as_view(), name="today"),
]
