from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, VendorProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class VendorRegistrationForm(UserCreationForm):
    store_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'store_name', 'phone_number', 'address']
