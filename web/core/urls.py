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
    path("logout/", views.user_logout, name="logout"),
    path("todo/create/", views.ToDoTaskCreateView.as_view(), name="todotaskcreate"),
    path("todo/list", views.ToDoListView.as_view(), name="todolist"),
    path("todo/check/<int:todo_id>", views.todo_check, name="todocheck"),
    path("todo/delete/<int:todo_id>", views.todo_delete, name="tododelete"),
    path("todo/detail/<int:pk>", views.ToDoTaskDetailView.as_view(), name="tododetail"),
    path("todo/update/<int:pk>", views.ToDoTaskUpdateView.as_view(), name="todoupdate")
]
