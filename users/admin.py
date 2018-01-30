from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from users.models import User


class UserAdmin(BaseUserAdmin):
	ordering = ('email',)
	readonly_fields=('date_created', 'date_updated','last_login' )
	
	list_display = ('email','name', 'is_superuser','is_staff','is_active','last_login', 'date_created', 'date_updated')
	
	
	fieldsets= (  (('Login Account'), {'fields':('email', 'password',)}),
				  (('Profile'), 	  {'fields':('name','avatar','company')}),
				  (('Dates'),         {'fields':('last_login','date_created', 'date_updated')} ),
				  (('Permissions'),   {'fields': ('is_active', 'is_superuser', 'is_staff')}),

				)

	
	add_fieldsets = (  (None, {
								'classes': ('wide'),
								'fields':('email','password1', 'password2',),
						      }
						),
					)
	
admin.site.register(User, UserAdmin)