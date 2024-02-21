"""
Module for configuring the core app.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuration class for the core app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
