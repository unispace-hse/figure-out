from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime


class SpacedLearningTask(models.Model):
    """Model representing a Spaced Learning Task."""

    MATERIAL_TYPE = [
        (0, "Nothing was new"),
        (1, "Almost nothing new"),
        (2, "Something was new"),
        (3, "Fifty/fifty new topic"),
        (4, "Mainly new topic"),
        (5, "Completely new topic"),
    ]
    GRADE_TYPE = [
        (0, "Perfect! Remember everything"),
        (1, "Not everything, but good enough"),
        (2, "I don't remember much"),
    ]
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="spacedlearningtasks"
    )
    title = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    new_material = models.IntegerField(choices=MATERIAL_TYPE, default=5)
    pages_cnt = models.IntegerField(
        default=1, validators=[MaxValueValidator(30), MinValueValidator(1)]
    )
    minutes_per_day = models.IntegerField(
        default=1, validators=[MaxValueValidator(2000), MinValueValidator(1)]
    )
    next_train_date = models.DateField(
        auto_now_add=False, default=datetime.date.today(), editable=False
    )
    prev_train_date = models.DateField(default=None, null=True)
    delta_days_daily = models.IntegerField(default=0)
    delta_days_const = models.IntegerField(default=10)
    rate = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)

    @property
    def is_ready_for_train_today(self):
        return SpacedLearningTask.objects.filter(
            pk=self.pk, next_train_date__lte=datetime.date.today()
        ).exists()

    def days_before_train(self):
        sl_task = SpacedLearningTask.objects.filter(pk=self.pk).first()
        delta = sl_task.next_train_date - datetime.date.today()
        sl_task.delta_days_daily = delta.days
        return str(delta.days)

    def percent_progress(self):
        sl_task = SpacedLearningTask.objects.filter(pk=self.pk).first()
        if sl_task.delta_days_const == 0:
            return "2"

        percent = (
            sl_task.delta_days_const - sl_task.delta_days_daily
        ) / sl_task.delta_days_const
        if percent < 0:
            return "100"
        elif percent == 0:
            return "10"
        elif percent > 100:
            return "10"
        else:
            return str(int(percent * 100))
