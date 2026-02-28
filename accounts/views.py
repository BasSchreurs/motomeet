# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone
from .forms import CustomSignUpForm, CustomLoginForm, ProfielForm
from .models import Profiel
from django.core.exceptions import ValidationError
import jwt  # PyJWT for Google ID token

# Hardcoded Google Client ID and local login URI
GOOGLE_CLIENT_ID = "426091807008-64gp6h66g97icjg5s9918afa48neh81t.apps.googleusercontent.com"
GOOGLE_LOGIN_URI = "http://127.0.0.1:8000/accounts/google-login/"  # must match Authorized redirect URI in Google Console


# ----------------------------
# Normal signup
# ----------------------------
def signup(request):
    login_uri = GOOGLE_LOGIN_URI

    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create Django user
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password1"],
                )

                # Auto-create/update Profiel
                profiel, _ = Profiel.objects.get_or_create(gebruikersnaam=user)
                profiel.geboortedatum = form.cleaned_data["geboortedatum"]
                profiel.woonplaats = form.cleaned_data["woonplaats"]
                profiel.motor_model = form.cleaned_data["motor_model"]
                profiel.save()

            # Log in user with explicit backend
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("complete_profile")
    else:
        form = CustomSignUpForm()

    return render(request, "accounts/account_signup.html", {"form": form, "login_uri": login_uri})


# ----------------------------
# Normal login
# ----------------------------
def login_view(request):
    login_uri = GOOGLE_LOGIN_URI

    # Use custom login form
    form = CustomLoginForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Use form.get_user() to get authenticated user
        user = form.get_user()
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect("home")

    return render(request, "accounts/account_login.html", {"form": form, "login_uri": login_uri})


# ----------------------------
# Google login callback
# ----------------------------
@csrf_exempt
def google_login(request):
    """
    Receives POST from Google Identity Services.
    Creates a user + Profiel if new, logs in otherwise.
    """
    if request.method == "POST":
        token = request.POST.get("credential")
        if not token:
            return redirect("signup")

        try:
            # Decode JWT from Google
            decoded = jwt.decode(token, options={"verify_signature": False})
            email = decoded.get("email")
            username = decoded.get("name") or email.split("@")[0]

            # Get or create Django user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": username}
            )

            # Ensure Profiel exists
            Profiel.objects.get_or_create(
                gebruikersnaam=user,
                defaults={"geboortedatum": None, "woonplaats": "", "motor_model": ""}
            )

            # Log in
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("check_profile")

        except Exception as e:
            print("Google login error:", e)
            return redirect("signup")

    return redirect("signup")


# ----------------------------
# Profile flow
# ----------------------------
@login_required
def complete_profile(request):
    profiel, _ = Profiel.objects.get_or_create(
        gebruikersnaam=request.user
    )

    if request.method == "POST":
        form = ProfielForm(request.POST, request.FILES, instance=profiel)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = ProfielForm(instance=profiel)

    return render(
        request,
        "accounts/complete_profile.html",
        {"form": form}
    )

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profiel = get_object_or_404(Profiel, gebruikersnaam=profile_user)
    
    # Show meetups user is attending
    attending_meetups = profile_user.meetups_attending.filter(
        start_date__gte=timezone.now()
    )
    
    # If viewing own profile, also show private meetups you're invited to but haven't joined yet
    if request.user == profile_user:
        invited_meetups = profile_user.invited_to_meetups.filter(
            start_date__gte=timezone.now()
        ).exclude(
            id__in=attending_meetups.values_list('id', flat=True)
        )
        
        # Combine attending and invited
        from itertools import chain
        meetups = sorted(
            chain(attending_meetups, invited_meetups),
            key=lambda x: x.start_date
        )
    else:
        # For other users, only show public meetups they're attending
        meetups = attending_meetups.filter(is_public=True).order_by('start_date')
    
    return render(request, "accounts/profile.html", {
        "profiel": profiel,
        "profile_user": profile_user,
        "meetups": meetups,
    })

@login_required
def check_profile(request):
    try:
        profiel = request.user.profiel
        if profiel.is_complete():
            return redirect("home")
        else:
            return redirect("complete_profile")
    except Profiel.DoesNotExist:
        return redirect("complete_profile")
    
@login_required
def voeg_vriend_toe(request, username):
    if request.method == 'POST':  # Only process POST requests
        andere_user = get_object_or_404(User, username=username)
        
        # Prevent adding yourself
        if andere_user != request.user:
            request.user.profiel.vrienden.add(andere_user)
        
        # Redirect back to the previous page (likely search results)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('home')

@login_required
def verwijder_vriend(request, username):
    if request.method == 'POST':
        andere_user = get_object_or_404(User, username=username)
        request.user.profiel.vrienden.remove(andere_user)
        
        # Redirect back to the previous page
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('home')