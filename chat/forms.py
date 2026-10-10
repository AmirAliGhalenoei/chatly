from django import forms
from .models import Conversation
from django.core.exceptions import ValidationError
from accounts.models import UserProfile

class CreateGroupForm(forms.Form):
    name = forms.CharField(max_length=80, required=True)

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Conversation.objects.filter(group_name = name).exists():
            raise ValidationError("این گروه با این نام از قبل وجود دارد")
        return name

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)
