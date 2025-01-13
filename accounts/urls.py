from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('add_balance/', views.add_balance, name='add_balance'),
    path('change-password/', PasswordChangeView.as_view(template_name='accounts/change_password.html'), name='change_password'),
    path('change-password/', auth_views.PasswordChangeView.as_view(success_url='/profile/'), name='password_change'),
    path('buy_plan/', views.buy_plan, name='buy_plan'),
]
