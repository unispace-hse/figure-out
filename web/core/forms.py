"""
Application forms
"""

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from . import models


class TagMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, tag: models.ToDoTag):
        return f"{tag.emoji}: {tag.title}"


class RegisterForm(UserCreationForm):
    gender = forms.ChoiceField(choices=models.Account.GENDER)
    birthday = forms.DateField(label="Birthday")

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "gender", "birthday")

    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        cd = self.cleaned_data
        account = models.Account(user=user, gender=cd.get("gender"), birthday=cd.get("birthday"))
        account.save()


class ToDoTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ToDoTaskForm, self).__init__(*args, **kwargs)
        self.fields["tags"].queryset = models.ToDoTag.objects.filter(user=self.request.user)

    class Meta:
        model = models.ToDoTask
        fields = ("title", "description", "notification_datetime", "tags", "priority_level")

    tags = TagMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class HabitForm(forms.ModelForm):
    class Meta:
        model = models.Habit
        fields = ("title", "description", "goal")