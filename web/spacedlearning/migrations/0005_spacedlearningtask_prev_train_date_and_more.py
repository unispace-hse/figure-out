# Generated by Django 4.2.10 on 2024-03-14 17:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spacedlearning", "0004_remove_spacedlearningtask_is_done"),
    ]

    operations = [
        migrations.AddField(
            model_name="spacedlearningtask",
            name="prev_train_date",
            field=models.DateField(default=None, null=True),
        ),
    ]
