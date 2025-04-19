from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form=UserAdd
    form=UserChange
    list_filter = ('is_active', 'is_admin')
    list_display=('mobile_number','is_active','is_admin')
    search_fields=('mobile_number',)
    
    ordering=('mobile_number',)
    fieldsets=(
        ('اطلاعات مهم',{'fields':('mobile_number','email','password',)}),
        ('اطلاعات فردی',{'fields':('name','family',)}),
        ('اطلاعات اکانت',{'fields':('activate_code','is_active','user_permissions','groups','is_superuser','is_admin')}),
    )
    add_fieldsets=(
        (None,{'fields':('mobile_number','name','family','password','password2')}),
    )
    filter_horizontal=('user_permissions','groups',)
    def get_actions(self, request):  
        actions = super().get_actions(request)  
        if 'reset_password' in actions:  
            del actions['reset_password']  # حذف دکمه Reset password  
        return actions 
admin.site.register(CustomUser,CustomUserAdmin)

@admin.register(Employer) 
class EmployerAdmin(admin.ModelAdmin):
    list_filter = ( 'user',)