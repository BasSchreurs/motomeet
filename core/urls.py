# core/urls.py
from django.urls import path
from django.views.generic.base import RedirectView
from .views import home
from accounts.views import signup, google_login, login_view
from . import views

urlpatterns = [
    path('', home, name='home'),

    # Custom login page
    path('login/', login_view, name='login'),  # points to your account_login.html view
    path('signup/', signup, name='signup'),  # custom signup page
    path('info/', views.info, name='info'),
    # Google Identity Services login endpoint
    path('accounts/google-login/', google_login, name='google_login'),
    path('search/', views.search_results, name='search_results'),
]