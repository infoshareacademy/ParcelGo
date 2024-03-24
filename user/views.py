from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.views import View



class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'user/register.html'  # Własny szablon HTML dla rejestracji
    success_url = '/login/'  # Po udanej rejestracji przekieruj na stronę logowania


class CustomLoginView(LoginView):
    template_name = 'user/login.html'

    def get_success_url(self):
        # Przekieruj użytkownika na stronę konta po zalogowaniu
        return reverse_lazy('user_account')


class CustomLogoutView(LogoutView):
    def get_next_page(self):
        # Przekieruj użytkownika na stronę główną po wylogowaniu
        return reverse_lazy('index')


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            fname = request.user.first_name
            return render(request, 'user/account.html', {'fname': fname})
        return render(request, 'user/index.html')


class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'user/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pobierz dane użytkownika lub wykonaj inne czynności związane z kontem użytkownika
        # Na przykład:
        user = self.request.user
        fname = user.first_name  # Pobierz imię użytkownika
        lname = user.last_name
        # tutaj miejsce na wiecej operacji z kontem

        context['fname'] = fname
        context['lname'] = lname
        # nowe dane do przekazania do szablonu
        return context
