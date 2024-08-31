from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@students.bju.edu'):
            raise ValidationError("You must use a BJU email address (e.g., name@students.bju.edu).")
        return email

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        full_name = self.cleaned_data['full_name']
        first_name, last_name = full_name.split(' ', 1)
        user.first_name = first_name
        user.last_name = last_name
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user