"""
Django models
"""

import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q
from . import habits_html_calendar
from .mlcontrol import Compute


class Account(models.Model):
    """Model extends base user model"""

    GENDER = [("M", "MALE"), ("F", "FEMALE"), ("O", "OTHER")]
    # Нумерация с нуля
    Q1 = [(i, i) for i in range(4)]
    Q2 = [(i, i) for i in range(16)]
    Q3 = [(i, i) for i in range(20)]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    birthday = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER, default="O")
    q1 = models.IntegerField(default=0, choices=Q1)
    q2 = ArrayField(models.IntegerField(choices=Q2), default=list)
    q3 = ArrayField(models.IntegerField(choices=Q3), default=list)

    @property
    def get_completed_todos_count(self):
        return ToDoTask.objects.filter(
            user=self.user, completed_at=datetime.date.today()
        ).count()

    @property
    def get_skipped_todos_count(self):
        return ToDoTask.objects.filter(
            Q(user=self.user)
            & Q(notification_date=datetime.date.today())
            & Q(completed_at__isnull=True)
        ).count()

    @property
    def get_completed_habits_count(self):
        return HabitDailyRecord.objects.filter(
            habit__user=self.user, date_completed=datetime.date.today()
        ).count()

    @property
    def get_skipped_habits_count(self):
        return (
            Habit.objects.filter(is_done=False).count()
            - self.get_completed_habits_count
            + HabitDailyRecord.objects.filter(
                date_completed=datetime.date.today(), habit__is_done=True
            ).count()
        )

    @property
    def get_age(self):
        return int((datetime.date.today() - self.birthday).days / 365)


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
    is_suggested = models.BooleanField(default=False)

    @property
    def is_completed_today(self):
        return HabitDailyRecord.objects.filter(
            habit=self, date_completed=datetime.date.today()
        ).exists()

    def change_completion(self):
        if self.is_completed_today:
            HabitDailyRecord.objects.filter(
                habit=self, date_completed=datetime.date.today()
            ).first().delete()
        else:
            HabitDailyRecord.objects.create(
                habit=self, date_completed=datetime.date.today()
            )

    @property
    def html_calendar(self):
        custom_calendar = habits_html_calendar.HabitsHTMLCalendar(
            self.created_at.date(),
            datetime.date.today() + datetime.timedelta(self.get_remaining_days),
        )
        if not self.is_completed_today:
            custom_calendar.end_date -= datetime.timedelta(1)
        return str(
            custom_calendar.formatmonth(
                datetime.date.today().year, datetime.date.today().month, withyear=True
            )
        )

    @property
    def get_remaining_days(self):
        return self.goal - HabitDailyRecord.objects.filter(habit=self).count()

    @staticmethod
    def get_save_suggested_habit(user):
        acc = Account.objects.get(user=user)
        title, typ, goal, idd = Compute.get_habit(acc.q3,
                                                  [],
                                                  age=acc.get_age)
        return Habit.objects.create(user=user, title=title, goal=goal, is_suggested=True)

    @staticmethod
    def update_suggested_habit(user):
        try:
            Habit.objects.filter(user=user, is_suggested=True).first().delete()
        except AttributeError:
            pass
        return Habit.get_save_suggested_habit(user)


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


class Event(models.Model):
    EVENT_TYPE = [
        (0, "Concert/Cinema/Theater"),
        (1, "Work or School"),
        (2, "Planned meeting with friends, co-workers"),
        (3, "Quality time in relationship"),
        (4, "Unplanned meeting after work/school"),
    ]

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="events"
    )
    title = models.CharField(max_length=128)
    type = models.IntegerField(choices=EVENT_TYPE, default=4)
    created_at = models.DateField(auto_now_add=True)
