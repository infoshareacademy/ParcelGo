from django.urls import path
from .views import CustomLogoutView, CustomLoginView, UserAccountView
from .views import SignUpView, LoginOrRegisterView

urlpatterns = [

    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', LoginOrRegisterView.as_view(), name='login_or_register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('account/', UserAccountView.as_view(), name='user_account'),


]