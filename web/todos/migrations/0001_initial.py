# Generated by Django 4.2.10 on 2024-03-05 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('emoji', models.CharField(max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todotags', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ToDoTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateField(null=True)),
                ('notification_date', models.DateTimeField(null=True)),
                ('priority_level', models.IntegerField(choices=[(0, 'No Priority'), (1, 'Low Priority'), (2, 'Medium Priority'), (3, 'High Priority')], default=0)),
                ('is_done', models.BooleanField(default=False)),
                ('tags', models.ManyToManyField(blank=True, related_name='tasks', to='todos.todotag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todotasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
