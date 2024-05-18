from django.urls import path
from .views import CustomLogoutView, CustomLoginView, UserAccountView
from .views import SignUpView, LoginOrRegisterView, change_username, ChangePasswordView, ChangeEmailView

urlpatterns = [
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', LoginOrRegisterView.as_view(), name='login_or_register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('account/', UserAccountView.as_view(), name='user_account'),
    path('change-username/', change_username, name='change_username_endpoint'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('change-email/', ChangeEmailView.as_view(), name='change_email'),

]
