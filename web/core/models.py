"""
Django models
"""

import datetime
from django.db import models
from django.contrib.auth import get_user_model
from . import habits_html_calendar


class Account(models.Model):
    """Model extends base user model"""

    GENDER = [
        ("M", "MALE"),
        ("F", "FEMALE"),
        ("O", "OTHER")
    ]
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    birthday = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        default="O"
    )


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
    updated_at = models.DateTimeField(auto_now=True)
    notification_datetime = models.DateTimeField(null=True)
    tags = models.ManyToManyField(ToDoTag, related_name="tasks", blank=True)
    priority_level = models.IntegerField(
        default=0,
        choices=PRIORITY_LEVEL
    )
    is_done = models.BooleanField(default=False)


class Habit(models.Model):
    """Model representing a habit."""

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="habits"
    )
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    goal = models.IntegerField(default=0)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_completed_today(self):
        return HabitDailyRecord.objects.filter(habit=self, date_completed=datetime.date.today()).exists()

    def change_completion(self):
        if self.is_completed_today:
            HabitDailyRecord.objects.filter(habit=self, date_completed=datetime.date.today()).first().delete()
        else:
            HabitDailyRecord.objects.create(habit=self, date_completed=datetime.date.today())

    @property
    def html_calendar(self):
        custom_calendar = habits_html_calendar.HabitsHTMLCalendar(self.created_at, self.created_at + datetime.timedelta(self.goal))
        return str(custom_calendar.formatmonth(datetime.date.today().year, datetime.date.today().month, withyear=True))


class HabitDailyRecord(models.Model):
    """Model representing daily records of completed habits."""

    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, related_name="habit_dailyrecords"
    )
    date_completed = models.DateField(db_index=True, auto_now_add=True)


class SpaceLearningTask(models.Model):
    """Model representing a task for space learning."""

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="spacelearningtasks"
    )
    title = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    is_done = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)


class SpaceLearningDailyRecord(models.Model):
    """Model representing daily records of space learning tasks."""

    task = models.ForeignKey(
        SpaceLearningTask,
        on_delete=models.CASCADE,
        related_name="spacelearningtask_dailyrecords",
    )
    notification_date = models.DateTimeField(db_index=True)
    is_checked = models.BooleanField(default=False)


class SpaceLearningFile(models.Model):
    """Model representing files related to space learning tasks."""

    task = models.ForeignKey(
        SpaceLearningTask, on_delete=models.CASCADE, related_name="files"
    )
    created_at = models.DateTimeField(auto_now_add=True)
