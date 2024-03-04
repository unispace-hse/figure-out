"""
Core views
"""
import datetime

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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

            return redirect("priorityservice")
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
        return models.ToDoTask.objects.filter(user=self.request.user).order_by("-notification_date")


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
    template_name = "core/tododetails.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.ToDoTask.objects.filter(user=self.request.user)
        else:
            return models.ToDoTask.none()


# class ToDoTaskUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.ToDoTask
#     template_name = "core/todocreate.html"
#     form_class = forms.ToDoTaskForm
#     # fields = ["title"]
#     success_url = reverse_lazy("todolist")
#
#     def get_form_kwargs(self):
#         kwargs = super(ToDoTaskUpdateView, self).get_form_kwargs()
#         kwargs["request"] = self.request
#         return kwargs


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
    return render(request, "core/todocreate.html", {"form": form})


class HabitsListView(LoginRequiredMixin, ListView):
    template_name = "core/habitslist.html"
    context_object_name = "habits_list"

    def get_queryset(self):
        return models.Habit.objects.filter(user=self.request.user)


class HabitDetailView(LoginRequiredMixin, DetailView):
    model = models.Habit
    template_name = "core/habitdetails.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.ToDoTask.none()


def habit_check(request, pk):
    habit = get_object_or_404(models.Habit, pk=pk)
    if habit.user != request.user:
        return Http404()
    habit.change_completion()
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
            form.save()
            return redirect("habitslist")
    form = forms.HabitForm(instance=obj)
    return render(request, "core/habitcreate.html", {"form": form})


@login_required
def setup_priority_service(request):
    if request.method == "POST":
        selected_choice = request.POST['choice']
        acc = models.Account.objects.filter(user=request.user).first()
        acc.q1 = int(selected_choice)
        acc.save()
        return redirect("character")
    return render(request, "core/setup_priority_service.html")


@login_required
def setup_character(request):
    # User have passed personalization test
    if models.Account.objects.filter(user=request.user).first().q2:
        return Http404()

    if request.method == "POST":
        arr = []
        for key, value in request.POST.dict().items():
            if key != "csrfmiddlewaretoken":
                arr.append(int(value))
        acc = models.Account.objects.filter(user=request.user).first()
        acc.q2 = arr
        acc.save()
        return redirect("experience")
    return render(request, "core/setup_character.html")


@login_required
def setup_experience(request):
    # User have passed personalization test
    if models.Account.objects.filter(user=request.user).first().q3:
        return Http404()

    if request.method == "POST":
        arr = []
        for key, value in request.POST.dict().items():
            if key != "csrfmiddlewaretoken":
                arr.append(int(value))
        acc = models.Account.objects.filter(user=request.user).first()
        acc.q3 = arr
        acc.save()
        return redirect("root")
    if (datetime.date.today() - models.Account.objects.filter(user=request.user).first().birthday).days/365.2425:
        age_category = 'a'
    else:
        age_category = 'b'
    return render(request, "core/setup_experience.html", context={"age_category": age_category})


class EventCreateView(CreateView):
    model = models.Event
    form_class = forms.EventForm
    success_url = reverse_lazy("today")
    template_name = "core/todays_feed.html"

    def get_context_data(self, **kwargs):
        completed_todos = models.ToDoTask.objects.filter(completed_at=datetime.date.today()).count()
        skipped_todos = models.ToDoTask.objects.filter(
            Q(notification_date=datetime.date.today()) & Q(completed_at__isnull=True)).count()
        kwargs["score"] = 9.45
        kwargs["skipped_todos"] = skipped_todos
        kwargs["completed_todos"] = completed_todos
        kwargs["skipped_habits"] = 3
        kwargs["completed_habits"] = 4
        kwargs["skipped_sl"] = 5
        kwargs["completed_sl"] = 6
        kwargs["events"] = models.Event.objects.filter(created_at=datetime.date.today())
        return super(EventCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect(self.success_url)
