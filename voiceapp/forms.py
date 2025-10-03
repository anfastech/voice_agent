# forms.py
from django import forms
from .models import VoiceUser

class VoiceUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    voice_note = forms.FileField(
        label='Record your voice',
        help_text='Record a short voice sample for authentication'
    )
    
    class Meta:
        model = VoiceUser
        fields = ['username', 'password', 'voice_note']