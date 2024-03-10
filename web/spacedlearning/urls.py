from django.urls import path
from . import views

urlpatterns = [
    path(
        "list/progress",
        views.SpacedLearningViewProgress.as_view(),
        name="spacedlearninglist_progress",
    ),
    path(
        "list/finished",
        views.SpacedLearningViewFinished.as_view(),
        name="spacedlearninglist_finished",
    ),
    path(
        "create", views.SpacedLearningCreateView.as_view(), name="spacedlearningcreate"
    ),
    path("delete/<int:pk>", views.spacedlearning_delete, name="spacedlearningdelete"),
    path(
        "detail/<int:pk>",
        views.SpacedLearningDetailView.as_view(),
        name="spacedlearningdetail",
    ),
    path(
        "update/<int:pk>",
        views.spacedlearning_task_update_view,
        name="spacedlearningupdate",
    ),
    path("grade/<int:pk>/<int:grade>", views.sl_grading_results, name="slgrade"),
]
