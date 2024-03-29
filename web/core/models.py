"""
Django models
"""

import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q
import habits.models
from api.control import get_grade


class Account(models.Model):
    """Model extends base user model"""

    GENDER = [("M", "MALE"), ("F", "FEMALE"), ("O", "OTHER")]
    # Нумерация с нуля
    Q1 = [(i, i) for i in range(4)]
    Q2 = [(i, i) for i in range(16)]
    Q3 = [(i, i) for i in range(20)]

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="account"
    )
    birthday = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER, default="O")
    q1 = models.IntegerField(default=0, choices=Q1)
    q2 = ArrayField(models.IntegerField(choices=Q2), default=list)
    q3 = ArrayField(models.IntegerField(choices=Q3), default=list)

    @property
    def get_completed_todos_count(self):
        return self.user.todotasks.filter(completed_at=datetime.date.today()).count()

    @property
    def get_skipped_todos_count(self):
        return self.user.todotasks.filter(
            Q(notification_date=datetime.date.today()) & Q(completed_at__isnull=True)
        ).count()

    @property
    def get_completed_habits_count(self):
        return habits.models.HabitDailyRecord.objects.filter(
            habit__user=self.user, date_completed=datetime.date.today()
        ).count()

    @property
    def get_skipped_habits_count(self):
        return (
            habits.models.Habit.objects.filter(
                user=self.user, is_done=False, is_suggested=False
            ).count()
            - self.get_completed_habits_count
            + habits.models.HabitDailyRecord.objects.filter(
                date_completed=datetime.date.today(),
                habit__is_done=True,
                habit__user=self.user,
            ).count()
        )

    @property
    def get_completed_sl_count(self):
        return self.user.spacedlearningtasks.filter(
            prev_train_date=datetime.date.today()
        ).count()

    @property
    def get_skipped_sl_count(self):
        return self.user.spacedlearningtasks.filter(
            next_train_date=datetime.date.today(), is_finished=False
        ).count()

    @property
    def get_grade(self):
        return get_grade(
            self.get_completed_sl_count,
            self.get_completed_todos_count,
            self.get_completed_habits_count,
            self.get_skipped_sl_count
            + self.get_skipped_todos_count
            + self.get_skipped_habits_count,
            list(
                self.user.events.filter(created_at=datetime.date.today()).values_list(
                    "type", flat=True
                )
            ),
        )

    @property
    def get_age(self):
        return int((datetime.date.today() - self.birthday).days / 365)


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
