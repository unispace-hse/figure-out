import datetime
from django.contrib.auth import get_user_model
from django.db import models
from core.models import Account
from . import habits_html_calendar
from .mlcontrol import Compute


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