"""
Core views
"""

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from . import forms


def user_login(request):
    """
    Handle user authentication and login.
    """
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                return HttpResponse("Disabled account")
            return HttpResponse("Invalid login")
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