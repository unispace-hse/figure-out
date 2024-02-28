"""
Core models for managing tasks and habits.
"""

from django.db import models
from django.contrib.auth import get_user_model


class ToDoTag(models.Model):
    """
    Represents a tag for a ToDoTask.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user who owns this ToDoTag.
    title : str
        The title of the ToDoTag.
    emoji : str
        The emoji associated with the ToDoTag.
    """

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="todotags"
    )
    title = models.CharField(max_length=32)
    emoji = models.CharField(max_length=1)


class ToDoTask(models.Model):
    """
    Represents a ToDoTask.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user who owns this ToDoTask.
    title : str
        The title of the ToDoTask.
    description : str, optional
        The description of the ToDoTask.
    created_at : datetime.datetime
        The date and time when the ToDoTask was created.
    updated_at : datetime.datetime
        The date and time when the ToDoTask was last updated.
    notification_datetime : datetime.datetime, optional
        The date and time when the notification for the ToDoTask is scheduled.
    tags : QuerySet of ToDoTag objects
        The tags associated with the ToDoTask.
    """

    PRIORITY_LEVEL = {
        0: "No Priority",
        1: "Low Priority",
        2: "Medium Priority",
        3: "High Priority",
    }
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="todotasks"
    )
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notification_datetime = models.DateTimeField(null=True)
    tags = models.ManyToManyField(ToDoTag, related_name="tasks")


class Habit(models.Model):
    """
    Represents a habit.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user who owns this Habit.
    title : str
        The title of the Habit.
    description : str, optional
        The description of the Habit.
    goal : int, optional
        The goal associated with the Habit.
    is_done : bool
        Indicates whether the Habit is done or not.
    created_at : datetime.datetime
        The date and time when the Habit was created.
    """

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="habits"
    )
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    goal = models.IntegerField(default=0)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class HabitDailyRecord(models.Model):
    """
    Represents a daily record for a habit.

    Parameters
    ----------
    habit : Habit
        The Habit associated with this HabitDailyRecord.
    date_completed : datetime.date
        The date when the Habit was completed.
    """

    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, related_name="habit_dailyrecords"
    )
    date_completed = models.DateField(db_index=True, auto_now_add=True)


class SpaceLearningTask(models.Model):
    """
    Represents a space learning task.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user who owns this SpaceLearningTask.
    title : str
        The title of the SpaceLearningTask.
    subject : str
        The subject of the SpaceLearningTask.
    is_done : bool
        Indicates whether the SpaceLearningTask is done or not.
    description : str, optional
        The description of the SpaceLearningTask.
    """

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="spacelearningtasks"
    )
    title = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    is_done = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)


class SpaceLearningDailyRecord(models.Model):
    """
    Represents a daily record for a space learning task.

    Parameters
    ----------
    task : SpaceLearningTask
        The SpaceLearningTask associated with this SpaceLearningDailyRecord.
    notification_date : datetime.datetime
        The date and time when the notification for the SpaceLearningTask is scheduled.
    is_checked : bool
        Indicates whether the SpaceLearningTask has been checked or not.
    """

    task = models.ForeignKey(
        SpaceLearningTask,
        on_delete=models.CASCADE,
        related_name="spacelearningtask_dailyrecords",
    )
    notification_date = models.DateTimeField(db_index=True)
    is_checked = models.BooleanField(default=False)


class SpaceLearningFile(models.Model):
    """
    Represents a file associated with a space learning task.

    Parameters
    ----------
    task : SpaceLearningTask
        The SpaceLearningTask associated with this SpaceLearningFile.
    created_at : datetime.datetime
        The date and time when the SpaceLearningFile was created.
    """

    task = models.ForeignKey(
        SpaceLearningTask, on_delete=models.CASCADE, related_name="files"
    )
    created_at = models.DateTimeField(auto_now_add=True)
