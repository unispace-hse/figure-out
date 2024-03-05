from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from . import models

class TagMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, tag: models.ToDoTag):
        return f"{tag.emoji}: {tag.title}"

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