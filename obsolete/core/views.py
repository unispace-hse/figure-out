"""
Module for defining views for the core app.
"""

from django.shortcuts import render


def home(request):
    """
    View function for rendering the home page.
    """
    return render(request, "sign_in.html")
