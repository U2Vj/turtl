from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

# Register your admin models here.
# Checkout https://docs.djangoproject.com/en/3.1/ref/contrib/admin/


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ["email"]}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "role",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "role", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "email", "role")
    list_filter = ("role", "groups")
    search_fields = ("username", "email")
