from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'verified', 'is_staff', 'date_joined']
    list_filter = ['verified', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    actions = ['verify_users', 'unverify_users']

    # Add 'verified' to the fieldsets shown when editing a user
    fieldsets = UserAdmin.fieldsets + (
        ('Verification', {'fields': ('verified',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Verification', {'fields': ('verified',)}),
    )

    def verify_users(self, request, queryset):
        updated = queryset.update(verified=True)
        self.message_user(request, f'{updated} user(s) verified successfully.')
    verify_users.short_description = 'Verify selected users (grant access)'

    def unverify_users(self, request, queryset):
        updated = queryset.update(verified=False)
        self.message_user(request, f'{updated} user(s) marked as unverified.')
    unverify_users.short_description = 'Revoke verification for selected users'
