from django import forms
from django.contrib.auth.models import User
from .models import Profiel
from django.contrib.auth import authenticate


class CustomSignUpForm(forms.ModelForm):
    username = forms.CharField(label="Gebruikersnaam")
    email = forms.EmailField(label="E-mailadres")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Wachtwoord")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Bevestig Wachtwoord")
    geboortedatum = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Geboortedatum")
    woonplaats = forms.CharField(max_length=100, label="Woonplaats")
    motor_model = forms.CharField(max_length=100, label="Motor Model")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error("password2", "Wachtwoorden komen niet overeen")
        return cleaned_data


class CustomLoginForm(forms.Form):
    login = forms.CharField(label="Gebruikersnaam of email")
    password = forms.CharField(label="Wachtwoord", widget=forms.PasswordInput)

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        login_input = cleaned_data.get("login")
        password = cleaned_data.get("password")

        if login_input and password:
            user = (
                User.objects.filter(username=login_input).first() or
                User.objects.filter(email=login_input).first()
            )
            if user is None:
                raise forms.ValidationError("Onbekende gebruiker")
            if not user.check_password(password):
                raise forms.ValidationError("Verkeerd wachtwoord")
            self.user = user

        return cleaned_data

    def get_user(self):
        return self.user


class ProfielForm(forms.ModelForm):
    geboortedatum = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        label="Geboortedatum"
    )

    class Meta:
        model = Profiel
        fields = [
            "geboortedatum", "woonplaats", "motor_model", "profiel_foto",
            "instagram", "facebook", "whatsapp", "youtube", "tiktok",
            "route_1_naam", "route_1",
            "route_2_naam", "route_2",
            "route_3_naam", "route_3",
            "route_4_naam", "route_4",
            "route_5_naam", "route_5",
        ]
        labels = {
            "woonplaats": "Woonplaats",
            "motor_model": "Motor Model",
            "instagram": "Instagram URL",
            "facebook": "Facebook URL",
            "whatsapp": "WhatsApp URL",
            "youtube": "YouTube URL",
            "tiktok": "TikTok URL",
            "route_1_naam": "Route 1 naam",
            "route_1": "Route 1 link",
            "route_2_naam": "Route 2 naam",
            "route_2": "Route 2 link",
            "route_3_naam": "Route 3 naam",
            "route_3": "Route 3 link",
            "route_4_naam": "Route 4 naam",
            "route_4": "Route 4 link",
            "route_5_naam": "Route 5 naam",
            "route_5": "Route 5 link",
        }
        widgets = {
            "instagram": forms.URLInput(attrs={"placeholder": "https://instagram.com/jouwprofiel"}),
            "facebook": forms.URLInput(attrs={"placeholder": "https://facebook.com/jouwprofiel"}),
            "whatsapp": forms.URLInput(attrs={"placeholder": "https://wa.me/31...jouwnummer"}),
            "youtube": forms.URLInput(attrs={"placeholder": "https://youtube.com/@jouwkanaal"}),
            "tiktok": forms.URLInput(attrs={"placeholder": "https://tiktok.com/@jouwprofiel"}),
            "route_1_naam": forms.TextInput(attrs={"placeholder": "Naam / Plaats..."}),
            "route_1": forms.URLInput(attrs={"placeholder": "Link naar route/kaart..."}),
            "route_2_naam": forms.TextInput(attrs={"placeholder": "Naam / Plaats..."}),
            "route_2": forms.URLInput(attrs={"placeholder": "Link naar route/kaart..."}),
            "route_3_naam": forms.TextInput(attrs={"placeholder": "Naam / Plaats..."}),
            "route_3": forms.URLInput(attrs={"placeholder": "Link naar route/kaart..."}),
            "route_4_naam": forms.TextInput(attrs={"placeholder": "Naam / Plaats..."}),
            "route_4": forms.URLInput(attrs={"placeholder": "Link naar route/kaart..."}),
            "route_5_naam": forms.TextInput(attrs={"placeholder": "Naam / Plaats..."}),
            "route_5": forms.URLInput(attrs={"placeholder": "Link naar route/kaart..."}),
        }