from django.shortcuts import render
from .forms import VoiceUserForm
from ..features.audio_processor import extract_real_audio_features

def index(request):
    analysis_result = None
    username = None
    voice_file = None
    
    if request.method == 'POST':
        form = VoiceUserForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            voice_note = form.cleaned_data['voice_note']
            
            try:
                # Read the entire file into memory
                file_content = b''.join([chunk for chunk in voice_note.chunks()])
                
                # Use REAL audio analysis with SpeechRecognition
                analysis_result = extract_real_audio_features(file_content, voice_note.name)
                voice_file = voice_note.name
                
            except Exception as e:
                analysis_result = {"error": f"Processing failed: {str(e)}"}
    else:
        form = VoiceUserForm()
    
    context = {
        'form': form,
        'analysis_result': analysis_result,
        'username': username,
        'voice_file': voice_file
    }
    return render(request, 'index.html', context)