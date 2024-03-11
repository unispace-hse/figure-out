import datetime
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from api.control import get_sl_data, get_sl_recap
from . import forms
from . import models


class SpacedLearningViewProgress(LoginRequiredMixin, ListView):
    template_name = "spacedlearning/spacedlearninglist_progress.html"
    context_object_name = "sl_list"

    def get_queryset(self):
        return models.SpacedLearningTask.objects.filter(
            user=self.request.user
        ).order_by("next_train_date")


class SpacedLearningViewFinished(LoginRequiredMixin, ListView):
    template_name = "spacedlearning/spacedlearninglist_finished.html"
    context_object_name = "sl_list"

    def get_queryset(self):
        return models.SpacedLearningTask.objects.filter(
            user=self.request.user
        ).order_by("created_at")


class SpacedLearningCreateView(LoginRequiredMixin, CreateView):
    model = models.SpacedLearningTask
    form_class = forms.SpacedLearningForm
    template_name = "spacedlearning/spacedlearningcreate.html"
    success_url = reverse_lazy("spacedlearninglist_progress")

    def form_valid(self, form):
        obj = form.save(commit=False)
        acc = self.request.user.account
        task_weight, rate, days_left = get_sl_data(
            obj.new_material, obj.pages_cnt, obj.minutes_per_day, acc.q1, acc.q2, 1
        )
        obj.delta_days_const = days_left
        obj.rate, obj.weight = rate, task_weight
        obj.next_train_date = datetime.date.today() + datetime.timedelta(
            days=obj.delta_days_const
        )
        obj.user = self.request.user
        obj.save()
        return redirect(self.success_url)


@login_required
def spacedlearning_delete(request, pk):
    sl_task = get_object_or_404(models.SpacedLearningTask, pk=pk)
    if sl_task.user != request.user:
        return Http404()
    sl_task.delete()
    return redirect("spacedlearninglist_progress")


@login_required
def spacedlearning_check(request, pk):
    sl_task = get_object_or_404(models.SpacedLearningTask, pk=pk)
    if sl_task.user != request.user:
        return Http404()
    sl_task.is_done = True
    sl_task.save()
    return redirect("spacedlearninglist_progress")


class SpacedLearningDetailView(LoginRequiredMixin, DetailView):
    model = models.SpacedLearningTask
    template_name = "spacedlearning/spacedlearningdetails.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.SpacedLearningTask.objects.filter(user=self.request.user)
        else:
            return models.SpacedLearningTask.none()


@login_required
def spacedlearning_task_update_view(request, pk):
    obj = get_object_or_404(models.SpacedLearningTask, id=pk)
    if obj.user != request.user:
        return Http404()
    if request.method == "POST":
        form = forms.SpacedLearningEditForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("spacedlearninglist_progress"))

    form = forms.SpacedLearningEditForm(instance=obj)
    return render(request, "spacedlearning/spacedlearningcreate.html", {"form": form})


@login_required
def sl_grading_results(request, pk, grade):
    sl_task = get_object_or_404(models.SpacedLearningTask, pk=pk)
    if sl_task.user != request.user:
        return Http404()

    sl_task.prev_train_date = datetime.date.today()

    weight, rate, new_delta = get_sl_recap(
        sl_task.rate, 1, sl_task.weight, sl_task.delta_days_const, grade
    )

    sl_task.weight, sl_task.rate = weight, rate

    if new_delta == -1:
        sl_task.is_finished = True
    else:
        sl_task.delta_days_const = new_delta
        sl_task.next_train_date = datetime.date.today() + datetime.timedelta(
            days=new_delta
        )
        sl_task.delta_days_daily = new_delta

    sl_task.save()

    return redirect("spacedlearninglist_progress")
