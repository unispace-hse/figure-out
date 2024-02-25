from django.db import models
from django.contrib.auth import get_user_model


class ToDoTag(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    emoji = models.CharField(max_length=1)


class ToDoTask(models.Model):
    PRIORITY_LEVEL = {
        0: "No Priority",
        1: "Low Priority",
        2: "Medium Priority",
        3: "High Priority"
    }
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notification_datetime = models.DateTimeField(null=True)
    tags = models.ManyToManyField(ToDoTag, related_name="tasks")
