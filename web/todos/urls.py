from django.urls import path
from . import views

urlpatterns = [
    # post views
    path("create", views.ToDoTaskCreateView.as_view(), name="todocreate"),
    path("list", views.ToDoListView.as_view(), name="todolist"),
    path("check/<int:todo_id>", views.todo_check, name="todocheck"),
    path("delete/<int:todo_id>", views.todo_delete, name="tododelete"),
    path("detail/<int:pk>", views.ToDoTaskDetailView.as_view(), name="tododetail"),
    path("update/<int:pk>", views.todo_task_update_view, name="todoupdate"),
]
