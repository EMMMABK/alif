from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import ngettext
from django.contrib import messages


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'surname', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('name', 'surname', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('OTP Info', {'fields': ('otp_secret',)}),  # Добавьте поле OTP Secret
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'surname', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    

    actions = ['change_password']

    def change_password(self, request, queryset):
        updated = 0
        for user in queryset:
            new_password = 'новый_пароль'
            user.set_password(new_password)
            user.save()
            updated += 1
        
        self.message_user(request, ngettext(
            '%d пароль успешно изменен.',
            '%d паролей успешно изменены.',
            updated,
        ) % updated, messages.SUCCESS)

    change_password.short_description = "Сменить пароль выбранным пользователям"

admin.site.register(User, CustomUserAdmin)
