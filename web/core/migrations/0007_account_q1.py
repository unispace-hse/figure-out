# Generated by Django 4.2.10 on 2024-03-02 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_account_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='q1',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3)], default=0),
        ),
    ]
