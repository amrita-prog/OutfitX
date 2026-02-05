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
        base = user.email.split('@')[0]
        user.username = f"{base}_{uuid.uuid4().hex[:4]}"
        user.roles = 'admin'

        if commit:
            user.save()
        
        return user
    

class SalesExecutiveSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email','full_name','phone','password1','password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        base = user.email.split('@')[0]
        user.username = f"{base}_{uuid.uuid4().hex[:4]}"
        user.roles = 'sales'

        if commit:
            user.save()

        return user
    

class InventoryManagerSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email','full_name','phone','password1','password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        base = user.email.split('@')[0]
        user.username = f"{base}_{uuid.uuid4().hex[:4]}"
        user.roles = 'inventory'

        if commit:
            user.save()

        return user

        