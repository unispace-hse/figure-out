# Generated by Django 4.2.10 on 2024-03-10 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habitdailyrecord",
            name="habit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="dailyrecords",
                related_query_name="dailyrecord",
                to="habits.habit",
            ),
        ),
    ]
