# Generated by Django 4.2.10 on 2024-03-04 11:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_event"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
