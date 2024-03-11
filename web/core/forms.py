"""
Application forms
"""

from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django import urls as us
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from . import models


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = us.reverse_lazy("signup")
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Sign up"))

    gender = forms.ChoiceField(choices=models.Account.GENDER)
    birthday = forms.DateField(
        label="Birthday",
        widget=forms.DateInput(attrs={"type": "date", "max": datetime.now().date()}),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "gender",
            "birthday",
        )

    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        cd = self.cleaned_data
        account = models.Account(
            user=user, gender=cd.get("gender"), birthday=cd.get("birthday")
        )
        account.save()


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit("submit", "Create Event"))

    class Meta:
        model = models.Event
        fields = ("title", "type")
