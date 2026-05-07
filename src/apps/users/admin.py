from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserOTPVerifications

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'is_active')
    list_editable = ("is_active", )

    search_fields = ('email', 'first_name', 'last_name', 'telegram_id')

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
        'first_name', 'last_name', 'telegram_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    ordering = ('date_joined',)

    readonly_fields = ('date_joined', 'last_login')


admin.site.register(User, UserAdmin)

admin.site.register(UserOTPVerifications)