# Generated by Django 4.2.10 on 2024-03-04 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_alter_event_created_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="todotask",
            old_name="notification_datetime",
            new_name="notification_date",
        ),
        migrations.RemoveField(
            model_name="todotask",
            name="updated_at",
        ),
        migrations.AddField(
            model_name="todotask",
            name="completed_at",
            field=models.DateField(null=True),
        ),
    ]
