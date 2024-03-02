"""
Core views
"""

from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from . import forms
from . import models


def index(request):
    return render(request, "core/home.html")


def user_login(request):
    """
    Handle user authentication and login.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("root")
        return render(request, "core/login.html", {"form": form})
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})


def user_signup(request):
    """
    Handle creating user account.
    """
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            # login user
            cd = form.cleaned_data
            user = authenticate(
                username=cd.get("username"),
                password=cd.get("password1")
            )
            login(request, user)

            return redirect("root")
        return render(request, "core/signup.html", {"form": form})
    form = forms.RegisterForm()
    return render(request, "core/signup.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("root")


class ToDoTaskCreateView(LoginRequiredMixin, CreateView):
    model = models.ToDoTask
    form_class = forms.ToDoTaskForm
    template_name = "core/todocreate.html"

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
    template_name = "core/todolist.html"
    context_object_name = "todo_list"

    def get_queryset(self):
        return models.ToDoTask.objects.filter(user=self.request.user).order_by("-notification_datetime")


@login_required
def todo_check(request, todo_id):
    todo = get_object_or_404(models.ToDoTask, pk=todo_id)
    if todo.user != request.user:
        return Http404
    todo.is_done = False if todo.is_done else True
    todo.save()

    return redirect("todolist")


@login_required
def todo_delete(request, todo_id):
    todo = get_object_or_404(models.ToDoTask, pk=todo_id)
    if todo.user != request.user:
        return Http404
    todo.delete()
    return redirect("todolist")


class ToDoTaskDetailView(LoginRequiredMixin, DetailView):
    model = models.ToDoTask
    template_name = "core/tododetails.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.ToDoTask.objects.filter(user=self.request.user)
        else:
            return models.ToDoTask.none()


class ToDoTaskUpdateView(LoginRequiredMixin, CreateView):
    model = models.ToDoTask
    form_class = forms.ToDoTaskForm
    template_name = "core/todocreate.html"

    success_url = reverse_lazy("todolist")

    def get_form_kwargs(self):
        kwargs = super(ToDoTaskUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
