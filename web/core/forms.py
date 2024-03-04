"""
Application forms
"""

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django import urls as us
from django.contrib.auth import get_user_model
from . import models
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class TagMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, tag: models.ToDoTag):
        return f"{tag.emoji}: {tag.title}"


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


class ToDoTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ToDoTaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit("submit", "Create task"))
        self.fields["tags"].queryset = models.ToDoTag.objects.filter(
            user=self.request.user
        )

    class Meta:
        model = models.ToDoTask
        fields = ("title", "description", "notification_date", "tags", "priority_level")

    tags = TagMultipleChoiceField(
        queryset=None, widget=forms.CheckboxSelectMultiple, required=False
    )
    notification_date = forms.DateField(
        label="Notification date", widget=forms.DateInput(attrs={"type": "date"})
    )


class HabitForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request")
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_action = us.reverse_lazy('root')
    #     self.helper.form_method = 'GET'
    #     self.helper.add_input(Submit('submit', 'Create task'))

    class Meta:
        model = models.Habit
        fields = ("title", "description", "goal")


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit("submit", "Create Event"))

    class Meta:
        model = models.Event
        fields = ("title", "type")
