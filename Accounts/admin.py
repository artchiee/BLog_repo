from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import ( User ,UserProfile)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from .forms import UserAdminChangeForm, UserAdminCreationForm

# Register your models here.
class UserAdmin(BaseUserAdmin):
# these fields used to create / change infos of users 
	create_form = UserAdminCreationForm
	change_form = UserAdminChangeForm
	
	list_display = ['get_user_full_name', 'email']
	list_select_related = True

	def get_user_full_name(self, instance):
		return User.email

	#list_display = ('email', 'admin')
	list_filter = ('admin_user', 'active_user', 'staff_user')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
	#('Personal info', {'fields' : () }),
		('Permissions', {'fields': ('admin_user', 'active_user', 'staff_user')}),
		)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
		'classes': ('wide',),
		'fields': ('email', 'password1', 'password2')}
		),
		)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()


admin.site.register(
User, UserAdmin
)

# Addding user profile to admin interface 
admin.site.register(UserProfile)

	# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)