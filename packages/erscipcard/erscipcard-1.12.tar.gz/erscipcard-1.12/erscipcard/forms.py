from django import forms
from .models import User1
from .widget import AvatarFileUploadInput

class User1form(forms.ModelForm):
    class Meta:
        model = User1
        fields = "__all__"
        widgets = {"pic": AvatarFileUploadInput }

