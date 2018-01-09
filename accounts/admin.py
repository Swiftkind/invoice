from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from accounts.models import Account

class UserAdmin(BaseUserAdmin):
    """ Modified the UserAdmin"""
    ordering = ('email',)

    list_display = ('email', 'is_superuser',)
    list_filter = ('is_superuser',)
    fieldsets = (
                    (None,                {'fields': ('email', 'password',) }),
                    (('Personal info'),   {'fields': ('first_name', 'last_name',)}),
                    (('Permissions'),     {'fields': ('is_active','is_superuser',)}),
                    #(('Important dates'), {'fields': ('date_joined',)}),
                )
    add_fieldsets = (
                        (None, {
                                'classes': ('wide',),
                                'fields': ('email', 'password1', 'password2',),
                                }),
                    )

admin.site.register(Account, UserAdmin)
