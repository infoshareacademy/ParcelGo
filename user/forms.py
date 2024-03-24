from django import forms
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

    email = forms.EmailField(label="Your Email address", max_length=100)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Your username"
        self.order_fields(['username', 'first_name', 'last_name', 'email', 'password1', 'password2'])

