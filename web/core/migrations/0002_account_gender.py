# Generated by Django 4.2.10 on 2024-02-26 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="gender",
            field=models.CharField(
                choices=[("M", "MALE"), ("F", "FEMALE"), ("O", "Other")],
                default="O",
                max_length=1,
            ),
        ),
    ]
