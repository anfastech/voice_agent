import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
import numpy as np
import tempfile
import os
import subprocess
import io

# Configure pydub to use FFmpeg
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffmpeg = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

print(f"🎯 FFmpeg configured: {AudioSegment.converter}")

def extract_real_audio_features(audio_data, filename):
    """
    REAL audio analysis using FFmpeg-enabled pydub
    """
    try:
        # Save audio data to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp_file:
            tmp_file.write(audio_data)
            temp_path = tmp_file.name
        
        wav_path = ""
        try:
            print(f"🔄 Processing: {filename}")
            
            # Method 1: Try pydub with FFmpeg
            try:
                audio = AudioSegment.from_file(temp_path)
                print(f"✅ Successfully loaded audio with pydub")
                print(f"   Duration: {len(audio)}ms, Channels: {audio.channels}, Sample Rate: {audio.frame_rate}")
                
            except Exception as e:
                print(f"❌ Pydub failed: {e}")
                # Method 2: Direct FFmpeg conversion
                wav_path = temp_path.replace('.webm', '.wav')
                convert_with_ffmpeg(temp_path, wav_path)
                audio = AudioSegment.from_wav(wav_path)
            
            # Convert to mono and standard sample rate
            audio = audio.set_channels(1).set_frame_rate(16000)
            
            # Export to WAV for consistent processing
            if not wav_path:
                wav_path = temp_path.replace('.webm', '.wav')
                audio.export(wav_path, format="wav")
            
            # Extract REAL features from audio
            features = analyze_audio_features(audio)
            
            # Try speech recognition
            speech_text = transcribe_speech(wav_path)
            
            features["speech_detected"] = len(speech_text) > 0 and "error" not in speech_text.lower() and "could not" not in speech_text.lower()
            features["spoken_text"] = speech_text
            features["analysis_method"] = "Real Audio Analysis (FFmpeg + SpeechRecognition)"
            features["ffmpeg_used"] = True
            features["file_processed"] = filename
            
            print(f"✅ Analysis complete - Energy: {features['energy']:.4f}, ZCR: {features['zero_crossing_rate']:.4f}")
            
            return features
            
        finally:
            # Clean up temporary files
            for path in [temp_path, wav_path]:
                if path and os.path.exists(path):
                    try:
                        os.unlink(path)
                    except Exception as e:
                        print(f"⚠️ Could not delete {path}: {e}")
                        
    except Exception as e:
        print(f"❌ Audio processing failed: {e}")
        return {"error": f"Audio processing failed: {str(e)}"}

def convert_with_ffmpeg(input_path, output_path):
    """
    Convert audio using direct FFmpeg command
    """
    try:
        cmd = [
            'ffmpeg', '-i', input_path,
            '-ac', '1',  # Mono
            '-ar', '16000',  # Sample rate
            '-y',  # Overwrite output
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise Exception(f"FFmpeg conversion failed: {result.stderr}")
        
        print("✅ FFmpeg conversion successful")
        
    except Exception as e:
        raise Exception(f"FFmpeg conversion error: {str(e)}")

def analyze_audio_features(audio_segment):
    """
    Extract real acoustic features from audio segment
    """
    try:
        # Get raw audio data as numpy array
        samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
        
        print(f"📊 Analyzing {len(samples)} samples...")
        
        # Normalize to [-1, 1]
        if audio_segment.sample_width == 2:  # 16-bit
            samples = samples / 32768.0
        elif audio_segment.sample_width == 1:  # 8-bit
            samples = (samples - 128) / 128.0
        else:  # 32-bit
            samples = samples / 2147483648.0
        
        # Remove silence (simple threshold)
        samples = remove_silence(samples)
        
        if len(samples) == 0:
            return {
                "energy": 0.0,
                "zero_crossing_rate": 0.0,
                "spectral_centroid": 0.0,
                "fundamental_frequency": 0.0,
                "voice_quality": "No audio detected - silence",
                "volume_level": "Silent",
                "pitch_level": "No pitch",
                "articulation": "No speech",
                "duration_seconds": 0.0,
                "sample_rate": audio_segment.frame_rate,
                "confidence": 0.0,
            }
        
        # 1. Energy (RMS) - REAL calculation
        energy = np.sqrt(np.mean(samples**2))
        
        # 2. Zero Crossing Rate - REAL calculation
        zero_crossings = np.sum(np.abs(np.diff(np.sign(samples)))) / 2
        zcr = zero_crossings / len(samples)
        
        # 3. Spectral Centroid - REAL FFT analysis
        fft = np.fft.fft(samples)
        frequencies = np.fft.fftfreq(len(fft), 1/audio_segment.frame_rate)
        magnitudes = np.abs(fft)
        
        # Only positive frequencies
        positive_freq_idx = frequencies > 0
        positive_freq = frequencies[positive_freq_idx]
        positive_mag = magnitudes[positive_freq_idx]
        
        if np.sum(positive_mag) > 0:
            spectral_centroid = np.sum(positive_freq * positive_mag) / np.sum(positive_mag)
        else:
            spectral_centroid = 0
        
        # 4. Fundamental Frequency (Pitch) - REAL calculation
        fundamental_freq = estimate_pitch(samples, audio_segment.frame_rate)
        
        # 5. Voice Quality Assessment based on REAL metrics
        if energy > 0.3:
            volume_level = "Loud"
        elif energy > 0.1:
            volume_level = "Medium"
        else:
            volume_level = "Quiet"
        
        if fundamental_freq > 200:
            pitch_level = "High Pitch"
        elif fundamental_freq > 120:
            pitch_level = "Medium Pitch"
        elif fundamental_freq > 0:
            pitch_level = "Low Pitch"
        else:
            pitch_level = "Unclear Pitch"
        
        if zcr > 0.1:
            articulation = "Clear Articulation"
        elif zcr > 0.05:
            articulation = "Normal Articulation"
        else:
            articulation = "Smooth Voice"
        
        # Overall voice quality
        if energy > 0.2 and 100 < fundamental_freq < 400 and zcr > 0.06:
            voice_quality = "Excellent - Clear and Well-balanced"
        elif energy > 0.1 and fundamental_freq > 0:
            voice_quality = "Good - Clear Voice"
        else:
            voice_quality = "Fair - Could be clearer"
        
        confidence = min(0.95, energy * 2 + (zcr * 2) + (min(fundamental_freq, 500) / 1000))
        
        return {
            "energy": float(energy),
            "zero_crossing_rate": float(zcr),
            "spectral_centroid": float(spectral_centroid),
            "fundamental_frequency": float(fundamental_freq),
            "voice_quality": voice_quality,
            "volume_level": volume_level,
            "pitch_level": pitch_level,
            "articulation": articulation,
            "duration_seconds": len(audio_segment) / 1000.0,
            "sample_rate": audio_segment.frame_rate,
            "confidence": float(confidence),
        }
        
    except Exception as e:
        print(f"❌ Feature analysis failed: {e}")
        raise

def remove_silence(samples, threshold=0.01):
    """
    Remove silent portions from audio
    """
    energy = np.sqrt(np.convolve(samples**2, np.ones(100)/100, mode='same'))
    return samples[energy > threshold]

def estimate_pitch(samples, sample_rate):
    """
    Estimate fundamental frequency using autocorrelation
    """
    try:
        # Apply windowing
        window = np.hanning(len(samples))
        windowed_samples = samples * window
        
        # Autocorrelation
        autocorr = np.correlate(windowed_samples, windowed_samples, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # Find peaks (skip the very beginning)
        peaks = []
        for i in range(20, len(autocorr) - 1):
            if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1]:
                peaks.append(i)
        
        if peaks:
            # Use the first significant peak as fundamental frequency
            fundamental_period = peaks[0]
            fundamental_freq = sample_rate / fundamental_period
            
            # Validate frequency range (human voice typically 80-400 Hz)
            if 80 <= fundamental_freq <= 400:
                return fundamental_freq
        
        return 0
        
    except Exception:
        return 0

def transcribe_speech(wav_path):
    """
    Use SpeechRecognition to transcribe spoken content
    """
    try:
        r = sr.Recognizer()
        
        with sr.AudioFile(wav_path) as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for the data
            audio_data = r.record(source)
            
            # Recognize speech
            text = r.recognize_google(audio_data)
            print(f"✅ Speech recognized: '{text}'")
            return text
            
    except sr.UnknownValueError:
        return "Could not understand audio - try speaking more clearly"
    except sr.RequestError as e:
        return f"Speech recognition service error: {e}"
    except Exception as e:
        return f"Speech recognition failed: {e}"