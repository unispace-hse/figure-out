# Generated by Django 4.2.10 on 2024-03-05 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_todotask_tags_remove_todotask_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habitdailyrecord',
            name='habit',
        ),
        migrations.DeleteModel(
            name='Habit',
        ),
        migrations.DeleteModel(
            name='HabitDailyRecord',
        ),
    ]