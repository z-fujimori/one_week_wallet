from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# admin.site.register(User, UserAdmin)  # Userモデルを登録
admin.site.unregister(Group)  # Groupモデルは不要のため非表示にします

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['account_id']  # ← usernameじゃなくaccount_idで並び替え
    list_display = ['account_id', 'email', 'is_staff', 'is_active']  # ← 表示項目もカスタム

    fieldsets = (
        (None, {'fields': ('account_id', 'email', 'password')}),
        ('Personal info', {'fields': ('username', 'last_name', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_id', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('account_id', 'email')

