# Generated by Django 4.2.10 on 2024-02-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_todotask_priority_level"),
    ]

    operations = [
        migrations.AddField(
            model_name="todotask",
            name="is_done",
            field=models.BooleanField(default=False),
        ),
    ]
