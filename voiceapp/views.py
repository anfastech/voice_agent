# views.py
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import VoiceUserForm
from .models import VoiceUser
import os
from django.conf import settings

def index_view(request):
    if request.method == 'POST':
        form = VoiceUserForm(request.POST, request.FILES)
        if form.is_valid():
            # Here Saves the user
            user = form.save()
            # Can add additional processing here
            messages.success(request, 'Registration successful!')
            return {'user': user}
            # return JsonResponse({  # ✅ JSON response for APIs
            #     'status': 'success',
            #     'user_id': user.id,
            #     'username': user.username
            # })
            # return render(request, 'success.html', {'user': user})
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VoiceUserForm()
    
    return render(request, 'theform.html', {'form': form})

# def result_view(request):
#     return render(request, 'success.html')