from django import forms
from .models import User, UserProfile
from django.contrib.auth.forms import (
    UserChangeForm as BaseUserChangeForm,
    UserCreationForm as BaseUserCreationForm 
)
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from django.core.exceptions import ValidationError
import re


# Custom User Forms
class UserCreationForm(BaseUserCreationForm):
    phone = forms.CharField(max_length=11)

    class Meta:
        model = User
        fields = BaseUserCreationForm.Meta.fields + ("phone",)


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ["phone", "username", "email"]

    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'] = JalaliDateField(
            label='تاریخ تولد',
            widget=AdminJalaliDateWidget,
            required=False,  # اگر می‌خواهید اجباری نباشد
        )       

# Login | Register | Forms
class UserLoginForm(forms.Form):
    phone = forms.CharField(label="phone")

    def clean_phone(self):
        pattern = r"^09\d{9}$"
        phone = self.cleaned_data["phone"]

        if len(phone) != 11:
            raise ValidationError("شماره تلفن نامعتبر است")
        elif not re.match(pattern, phone):
            raise ValidationError("شماره تلفن نامعتبر است")

        return phone

class UserLoginVerifyForm(forms.Form):
    code = forms.CharField(max_length=6, label="code")

class UserRegisterForm(forms.Form):
    phone = forms.CharField(max_length=11, label="phone")
    username = forms.CharField(max_length=150, label="username")

    def clean_phone(self):
        pattern = r"^09\d{9}$"
        phone = self.cleaned_data["phone"]

        if User.objects.filter(phone=phone).exists():
            raise ValidationError("این کاربر از قبل وجود دارد")
        elif len(phone) != 11:
            raise ValidationError("شماره تلفن نامعتبر است")
        elif not re.match(pattern, phone):
            raise ValidationError("شماره تلفن نامعتبر است")
        return phone

class UserRegisterVerifyForm(forms.Form):
    code = forms.CharField(max_length=6, label="code")


    

