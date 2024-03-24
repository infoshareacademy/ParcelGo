from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
UserModel = get_user_model()

class UserCreationForm(forms.ModelForm):
    """Formularz do tworzenia nowych użytkowników."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ["email", "first_name", "last_name"]

    def clean_password2(self):
        # Sprawdź, czy oba wprowadzone hasła są takie same
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Zapisz hasło w postaci zaszyfrowanej
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Formularz do aktualizacji użytkowników."""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserModel
        fields = ["email", "password", "first_name", "last_name", "is_active"]


class UserAdmin(BaseUserAdmin):
    """Konfiguracja panelu administratora dla modelu MyUser."""

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "first_name", "last_name"]

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name"]}),

    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name", "last_name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(UserModel, UserAdmin)



