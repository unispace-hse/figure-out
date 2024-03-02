"""
Core views
"""

from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
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

            return redirect("login")
        return render(request, "core/signup.html", {"form": form})
    form = forms.RegisterForm()
    return render(request, "core/signup.html", {"form": form})


# def todotask_create(request):
#     form = forms.ToDoTaskForm()
#     return render(request, "core/todocreate.html", context={"form": form})

class AddToDoTask(CreateView):
    model = models.ToDoTask
    form_class = forms.ToDoTaskForm
    template_name = "core/todocreate.html"
    success_url = reverse_lazy("root")

    def get_form_kwargs(self):
        kwargs = super(AddToDoTask, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


def user_logout(request):
    logout(request)
    return redirect("root")
