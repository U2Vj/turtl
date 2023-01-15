from django.contrib import admin
from .models import User


# Register your admin models here.
# Checkout https://docs.djangoproject.com/en/3.1/ref/contrib/admin/

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'get_Roles']

    def get_Roles(self, obj):
        return "\n".join([p.name for p in obj.groups.all()])

