from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from . import forms


class HabitsListView(LoginRequiredMixin, ListView):
    template_name = "core/habitslist.html"
    context_object_name = "habits_list"

    def get_queryset(self):
        return models.Habit.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs["suggested"] = models.Habit.update_suggested_habit(self.request.user)
        return super(HabitsListView, self).get_context_data(object_list=object_list, **kwargs)


class HabitDetailView(LoginRequiredMixin, DetailView):
    model = models.Habit
    template_name = "core/habitdetails.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.none()


def habit_check(request, pk):
    habit = get_object_or_404(models.Habit, pk=pk)
    if habit.user != request.user:
        return Http404()
    habit.change_completion()

    habit.is_done = habit.get_remaining_days == 0
    habit.save()
    return redirect("habitslist")


def habit_delete(request, pk):
    habit = get_object_or_404(models.Habit, pk=pk)
    if habit.user != request.user:
        return Http404()
    habit.delete()
    return redirect("habitslist")


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = models.Habit
    form_class = forms.HabitForm
    template_name = "core/habitcreate.html"

    success_url = reverse_lazy("habitslist")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect(self.success_url)


@login_required
def habit_update_view(request, pk):
    obj = get_object_or_404(models.Habit, id=pk)
    if obj.user != request.user:
        return Http404()
    if request.method == "POST":
        form = forms.HabitForm(request.POST, instance=obj)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.is_suggested = False
            habit.save()
            return redirect("habitslist")
    form = forms.HabitForm(instance=obj)
    return render(request, "core/habitcreate.html", {"form": form})
