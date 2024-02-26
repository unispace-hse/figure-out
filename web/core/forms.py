"""
Application forms
"""

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from . import models


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
