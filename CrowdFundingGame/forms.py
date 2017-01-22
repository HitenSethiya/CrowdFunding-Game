from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class SignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    password_repeat = forms.CharField(label="Re-enter Password", max_length=30,
                                      widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password2'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('college', 'type')


class TransactionForm(forms.Form):  # error
    send_to = forms.ModelChoiceField(queryset=User.objects.filter(profile__type__exact='P'))
    money = forms.IntegerField(label="Money",
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'name': 'money'}))

    def valid_transaction(self):
        money = self.cleaned_data['money']
        if money < 0:
            self._errors["money"] = ["Invalid Amount"]  # Will raise a error message
