from django import forms
import os

class AvatarFileUploadInput(forms.ClearableFileInput):
    template_name = "AvatarFileUploadInput.html"
    def get_context(self, name, value, attrs):
        if value:
            value.name = os.path.basename(value.name)
        context = super().get_context(name, value, attrs)       
        return context
