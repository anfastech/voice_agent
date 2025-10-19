# forms.py
from django import forms
from .models import VoiceUser

class VoiceUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Enter your password',
            'required': 'true'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Enter your username',
            'required': 'true'
        })
    )
    
    voice_note = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'accept': 'audio/*',
            'required': 'true'
        }),
        label='Voice Recording',
        help_text='Record a short voice sample for authentication'
    )
    
    
    """
    BACKUP CODE:
    password = forms.CharField(widget=forms.PasswordInput)
    voice_note = forms.FileField(
        label='Record your voice',
        help_text='Record a short voice sample for authentication'
    )
    
    """
    
    class Meta:
        model = VoiceUser
        fields = ['username', 'password', 'voice_note']