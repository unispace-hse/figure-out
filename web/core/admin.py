"""
Django admin
"""

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from . import models


class AccountInLine(admin.StackedInline):
    """Inline Account model"""

    model = models.Account
    can_delete = False
    verbose_name_plural = "Accounts"


class CustomizedUserAdmin(UserAdmin):
    """
    Customized UserAdmin
    """

    inlines = (AccountInLine, )


admin.site.unregister(Group)
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomizedUserAdmin)
