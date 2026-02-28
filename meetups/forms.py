from django import forms
from .models import Meetup, Comment
from django.contrib.auth.models import User

class MeetupForm(forms.ModelForm):
    is_public = forms.BooleanField(
        required=False,
        initial=True,
        label="Publieke Meetup",
        help_text="Vink uit om deze meetup privé te maken (alleen voor uitgenodigde vrienden)"
    )
    
    invited_friends = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # Will be set in __init__
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Vrienden Uitnodigen",
        help_text="Selecteer vrienden om uit te nodigen (alleen voor private meetups)"
    )
    
    class Meta:
        model = Meetup
        fields = ['title', 'description', 'location', 'start_date', 'end_date', 'image', 'route_link', 'document_link', 'is_public', 'invited_friends']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only show user's friends in the invited_friends field
        if user:
            self.fields['invited_friends'].queryset = user.profiel.vrienden.all()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Schrijf een reactie...'}),
        }
        labels = {
            'body': '',
        }