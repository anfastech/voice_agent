# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import VoiceUserForm
from .models import VoiceUser
import os
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = VoiceUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return render(request, 'success.html', {'user': user})
    else:
        form = VoiceUserForm()
    
    return render(request, 'index.html', {'form': form})

def success(request):
    return render(request, 'success.html')