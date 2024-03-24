from django.urls import path
from .views import CustomLogoutView, CustomLoginView, UserAccountView
from .views import SignUpView, HomeView

urlpatterns = [

    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('account/', UserAccountView.as_view(), name='user_account'),


]