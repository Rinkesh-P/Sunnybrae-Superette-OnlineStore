from django import forms 
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CheckoutInfo

#All forms will go here, easy to maintain. 

class LoginForm(forms.Form):
    username = forms.CharField(widget=TextInput(attrs={
        'class': "form-control", 
        'style': 'max-width: 300px;',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=PasswordInput(attrs={
        'class': "form-control", 
        'style': 'max-width: 300px;',
        'placeholder': 'Password'
    }))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=EmailInput(attrs={
        'class': "form-control", 
        'style': 'max-width: 300px;',
        'placeholder': 'Email'
    }))

    password1 = forms.CharField(widget=PasswordInput(attrs={
        'class': "form-control",
        'style': 'max-width: 300px;',
        'placeholder': 'Password'
    }))

    password2 = forms.CharField(widget=PasswordInput(attrs={
        'class': "form-control",
        'style': 'max-width: 300px;',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Username'
            }),
        }

class RegisteredCheckoutForm(forms.ModelForm):
    class Meta:
        model = CheckoutInfo
        fields = ['address', 'city', 'suburb', 'zipcode', 'country']
        widgets = {
            'address': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Address'
            }),
            'city': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'City'
            }),
            'suburb': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Suburb'
            }),
            'zipcode': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Zipcode'
            }),
            'country': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Country'
            }),
        }

class GuestCheckoutForm(forms.ModelForm):
    guest_email = forms.EmailField(widget=EmailInput(attrs={
        'class': "form-control",
        'style': 'max-width: 300px;',
        'placeholder': 'Enter Email'
    }))
    class Meta:
        model = CheckoutInfo
        fields = ['guest_email', 'address', 'city', 'suburb', 'zipcode', 'country']
        widgets = {
            'address': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Address'
            }),
            'city': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'City'
            }),
            'suburb': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Suburb'
            }),
            'zipcode': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Zipcode'
            }),
            'country': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Country'
            }),
        }