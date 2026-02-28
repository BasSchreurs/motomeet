# accounts/urls.py
from django.urls import path
from .views import signup, login_view, profile_view
from . import views

urlpatterns = [
    path('signup/', signup, name='signup'),  # your custom signup
    path('login/', login_view, name='login'),  # use custom login view
    path("check-profile/", views.check_profile, name="check_profile"),
    path("complete-profile/", views.complete_profile, name="complete_profile"),
    path("google-login/", views.google_login, name="google_login"),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('vriend/toevoegen/<str:username>/', views.voeg_vriend_toe, name='voeg_vriend_toe'),
    path('vriend/verwijderen/<str:username>/', views.verwijder_vriend, name='verwijder_vriend'),
]