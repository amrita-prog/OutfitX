from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
import uuid

class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user= super().save(commit=False)
        base_username = user.email.split('@')[0]
        user.username = f"{base_username}_{uuid.uuid4().hex[:4]}"
        user.roles = 'admin'

        