# Generated by Django 4.2.10 on 2024-03-04 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_event_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
