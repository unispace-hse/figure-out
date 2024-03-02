"""
Application forms
"""

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from . import models
from datetime import  datetime
from crispy_forms.helper import FormHelper


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, member):
        return "%s" % member.title


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    gender = forms.ChoiceField(choices=models.Account.GENDER)
    birthday = forms.DateField(label="Birthday", widget=forms.DateInput(attrs={'type': 'date',
                                                                               'max': datetime.now().date()}))


    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "gender", "birthday")

    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        cd = self.cleaned_data
        account = models.Account(user=user, gender=cd.get("gender"), birthday=cd.get("birthday"))
        account.save()


class ToDoTaskForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        self.request = kwargs.pop("request")
        super(ToDoTaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["tags"].queryset = models.ToDoTag.objects.filter(user=self.request.user)

    class Meta:
        model = models.ToDoTask
        fields = ("title", "description", "notification_datetime", "tags", "priority_level")

    tags = CustomModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )
