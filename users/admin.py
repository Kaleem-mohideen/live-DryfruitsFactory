from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .forms import *


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    model = get_user_model()
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'phone_number', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'phone_number', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(get_user_model(), CustomUserAdmin)
