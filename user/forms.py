from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
User = get_user_model()

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Your username"
        self.order_fields(['username', 'first_name', 'last_name', 'email', 'password1', 'password2'])
        self.fields['password1'].help_text = None
        self.fields['username'].widget.attrs['autocomplete'] = 'username'
        self.fields['password1'].widget.attrs['autocomplete'] = 'new-password'
        self.fields['password2'].widget.attrs['autocomplete'] = 'new-password'
        self.fields['email'].widget.attrs['autocomplete'] = 'email'
        self.fields['first_name'].widget.attrs['autocomplete'] = 'given-name'

class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(max_length=150, label='New Username')

    def clean_new_username(self):
        new_username = self.cleaned_data['new_username']
        if User.objects.filter(username=new_username).exists():
            raise ValidationError("Username already exists.")
        return new_username

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'Current Password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'

class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(max_length=254, label='New Email')

    def clean_new_email(self):
        new_email = self.cleaned_data['new_email']
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("Email already exists.")
        return new_email

