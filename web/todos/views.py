import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView

from . import models
from . import forms


# Create your views here.
class ToDoTaskCreateView(LoginRequiredMixin, CreateView):
    model = models.ToDoTask
    form_class = forms.ToDoTaskForm
    template_name = "todos/todocreate.html"

    success_url = reverse_lazy("todolist")

    def get_form_kwargs(self):
        kwargs = super(ToDoTaskCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect(self.success_url)


class ToDoListView(LoginRequiredMixin, ListView):
    template_name = "todos/todolist.html"
    context_object_name = "todo_list"

    def get_queryset(self):
        return models.ToDoTask.objects.filter(user=self.request.user).order_by(
            "-notification_date"
        )


@login_required
def todo_check(request, todo_id):
    todo = get_object_or_404(models.ToDoTask, pk=todo_id)
    if todo.user != request.user:
        return Http404()
    if todo.is_done:
        todo.is_done = False
        todo.completed_at = None
    else:
        todo.is_done = True
        todo.completed_at = datetime.date.today()
    todo.save()

    return redirect("todolist")


@login_required
def todo_delete(request, todo_id):
    todo = get_object_or_404(models.ToDoTask, pk=todo_id)
    if todo.user != request.user:
        return Http404()
    todo.delete()
    return redirect("todolist")


class ToDoTaskDetailView(LoginRequiredMixin, DetailView):
    model = models.ToDoTask
    template_name = "todos/tododetails.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.ToDoTask.objects.filter(user=self.request.user)
        else:
            return models.ToDoTask.none()


@login_required
def todo_task_update_view(request, pk):
    obj = get_object_or_404(models.ToDoTask, id=pk)
    if obj.user != request.user:
        return Http404()
    if request.method == "POST":
        form = forms.ToDoTaskForm(request.POST, instance=obj, request=request)
        if form.is_valid():
            form.save()
            return redirect("todolist")
    form = forms.ToDoTaskForm(instance=obj, request=request)
    return render(request, "todos/todocreate.html", {"form": form})
