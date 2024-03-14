from django import forms
from . import models


class SpacedLearningForm(forms.ModelForm):
    class Meta:
        model = models.SpacedLearningTask
        fields = (
            "title",
            "description",
            "subject",
            "new_material",
            "pages_cnt",
            "minutes_per_day",
        )


class SpacedLearningEditForm(forms.ModelForm):
    class Meta:
        model = models.SpacedLearningTask
        fields = ("title", "description", "subject")
