from django.urls import path
from . import views

urlpatterns = [
    path("list", views.HabitsListView.as_view(), name="habitslist"),
    path("detail/<int:pk>", views.HabitDetailView.as_view(), name="habitdetail"),
    path("check/<int:pk>", views.habit_check, name="habitcheck"),
    path("create", views.HabitCreateView.as_view(), name="habitcreate"),
    path("update/<int:pk>", views.habit_update_view, name="habitupdate"),
    path("delete/<int:pk>", views.habit_delete, name="habitdelete"),
]
