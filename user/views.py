from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'user/register.html'  # Własny szablon HTML dla rejestracji
    success_url = '/users/login/'  # Po udanej rejestracji przekieruj na stronę logowania


class CustomLoginView(LoginView):
    template_name = 'user/login.html'

    def get_success_url(self):
        # Przekieruj użytkownika na stronę konta po zalogowaniu
        return reverse_lazy('user_account')


class CustomLogoutView(LogoutView):
    def get_next_page(self):
        # Przekieruj użytkownika na stronę logowania po wylogowaniu
        return reverse_lazy('login_or_register')


class LoginOrRegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            fname = request.user.first_name
            return render(request, 'user/account.html', {'fname': fname})
        return render(request, 'user/login_or_register.html')


class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'user/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pobierz dane użytkownika
        user = self.request.user
        fname = user.first_name  # Pobierz imię użytkownika
        lname = user.last_name

        context['fname'] = fname
        context['lname'] = lname
        # nowe dane do przekazania do szablonu
        return context


def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')

        if not new_username:
            error_message = 'Username cannot be empty.'
            return JsonResponse({'success': False, 'error': error_message})

        if User.objects.filter(username=new_username).exists():
            error_message = 'This username is already taken please choose another one.'
            return JsonResponse({'success': False, 'error': error_message})

        user = request.user

        user.username = new_username
        user.save()

        return JsonResponse({'success': True})
    else:
        error_message = 'Invalid request method'
        return JsonResponse({'success': False, 'error': error_message})

class ChangePasswordView(View):
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Aktualizuj sesję użytkownika po zmianie hasła
            update_session_auth_hash(request, user)
            return JsonResponse({'success': True})
        else:
            # Jeśli formularz nie jest poprawny, zwróć błędy dla każdego pola osobno
            errors = form.errors.get_json_data()
            return JsonResponse({'success': False, 'errors': errors})

class ChangeEmailView(View):
    def post(self, request, *args, **kwargs):
        new_email = request.POST.get('new_email')
        user = request.user

        if not new_email:
            error_message = 'Email address cannot be empty.'
            return JsonResponse({'success': False, 'error': error_message})

        # Sprawdź, czy nowy adres email nie jest już używany przez innego użytkownika
        if User.objects.filter(email=new_email).exists():
            error_message = 'This email address is already associated with another account.'
            return JsonResponse({'success': False, 'error': error_message})

        # Zaktualizuj adres email użytkownika
        user.email = new_email
        user.save()

        return JsonResponse({'success': True})
