# Generated by Django 4.2.10 on 2024-03-10 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spacedlearning", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="spacedlearningtask",
            name="rate",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="spacedlearningtask",
            name="weight",
            field=models.FloatField(default=0.0),
        ),
    ]
