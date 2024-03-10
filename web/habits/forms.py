from django import forms
from . import models


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
