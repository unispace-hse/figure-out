# Generated by Django 4.2.10 on 2024-03-10 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0017_remove_habitdailyrecord_habit_delete_habit_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="spacelearningfile",
            name="task",
        ),
        migrations.RemoveField(
            model_name="spacelearningtask",
            name="user",
        ),
        migrations.AlterField(
            model_name="account",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="account",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="SpaceLearningDailyRecord",
        ),
        migrations.DeleteModel(
            name="SpaceLearningFile",
        ),
        migrations.DeleteModel(
            name="SpaceLearningTask",
        ),
    ]