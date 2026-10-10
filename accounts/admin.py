from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm, UserProfileForm

from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
 
# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        ("Information User",{"fields":("phone", "email", "username")}),
        ("Permissions",{"fields":("is_active", "is_staff", "is_superuser")}),
        ("Last Login",{"fields":("last_login",)}),
    )

    add_fieldsets = (
        ("Create User", {"fields":("phone","email","username", "password1", "password2")}),
    )
admin.site.register(User,UserAdmin)
admin.site.unregister(Group)


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    form = UserProfileForm
    
    list_display = ('user', 'username_id', 'age', 'get_date_of_birth_jalali')
    search_fields = ('user__username', 'username_id')
    list_filter = ('age',)
    
    @admin.display(description='تاریخ تولد')
    def get_date_of_birth_jalali(self, obj):
        if obj.date_of_birth:
            return datetime2jalali(obj.date_of_birth).strftime('%Y/%m/%d')
        return '-'