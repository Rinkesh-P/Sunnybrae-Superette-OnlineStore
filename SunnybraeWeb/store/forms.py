from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CheckoutInfo

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RegisteredCheckoutForm(forms.ModelForm):
    class Meta:
        model = CheckoutInfo
        fields = ['address', 'city', 'suburb', 'zipcode', 'country']

class GuestCheckoutForm(forms.ModelForm):
    guest_email = forms.EmailField()

    class Meta:
        model = CheckoutInfo
        fields = ['guest_email', 'address', 'city', 'suburb', 'zipcode', 'country']
