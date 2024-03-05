from django.contrib.auth import get_user_model
from django.db import models


class ToDoTag(models.Model):
    """Model representing a tag for ToDoTask."""

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="todotags"
    )
    title = models.CharField(max_length=32)
    emoji = models.CharField(max_length=1)


class ToDoTask(models.Model):
    """Model representing a ToDoTask."""

    PRIORITY_LEVEL = (
        (0, "No Priority"),
        (1, "Low Priority"),
        (2, "Medium Priority"),
        (3, "High Priority"),
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="todotasks"
    )
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateField(null=True)
    notification_date = models.DateTimeField(null=True)
    tags = models.ManyToManyField(ToDoTag, related_name="tasks", blank=True)
    priority_level = models.IntegerField(default=0, choices=PRIORITY_LEVEL)
    is_done = models.BooleanField(default=False)
