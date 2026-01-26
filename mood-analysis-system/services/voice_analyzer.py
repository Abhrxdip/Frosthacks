# =============================================================================
# services/voice_analyzer.py
# Analyzes voice emotion from audio file
# =============================================================================

import librosa
import numpy as np
import parselmouth
from parselmouth.praat import call
import warnings
warnings.filterwarnings('ignore')


class VoiceAnalyzer:
    """
    Extracts emotional features from voice audio.
    
    Returns mood score 1-10 based on:
    - Pitch (how high/low voice is)
    - Jitter (voice stability)
    - Shimmer (voice quality)
    - Speaking rate (words per minute)
    - Energy (loudness/intensity)
    """
    
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
    
    def analyze(self, audio_path: str) -> dict:
        """
        Analyze voice from audio file.
        
        Args:
            audio_path: Path to audio file (WAV, MP3, etc.)
            
        Returns:
            {
                'moodScore': float (1-10),
                'confidence': float (0-1),
                'features': dict
            }
        """
        print(f"🎤 Analyzing voice from: {audio_path}")
        
        try:
            # Load audio
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            sound = parselmouth.Sound(audio_path)
            
            # Extract features
            features = {
                'pitch': self._get_pitch(sound),
                'jitter': self._get_jitter(sound),
                'shimmer': self._get_shimmer(sound),
                'speaking_rate': self._get_speaking_rate(audio, sr),
                'energy': self._get_energy(audio)
            }
            
            # Calculate mood score
            mood_score = self._calculate_mood(features)
            confidence = self._calculate_confidence(features)
            
            print(f"   Voice Mood: {mood_score}/10 (confidence: {confidence:.2f})")
            
            return {
                'moodScore': round(mood_score, 2),
                'confidence': round(confidence, 2),
                'features': features
            }
            
        except Exception as e:
            print(f"   ⚠️ Voice analysis failed: {e}")
            return {
                'moodScore': 5.0,  # Neutral fallback
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _get_pitch(self, sound):
        """Extract pitch (F0) statistics."""
        pitch = call(sound, "To Pitch", 0.0, 75, 600)
        pitch_values = pitch.selected_array['frequency']
        pitch_values = pitch_values[pitch_values != 0]
        
        if len(pitch_values) == 0:
            return {'mean': 0, 'std': 0}
        
        return {
            'mean': float(np.mean(pitch_values)),
            'std': float(np.std(pitch_values))
        }
    
    def _get_jitter(self, sound):
        """Voice instability (higher = more stressed)."""
        try:
            point_process = call(sound, "To PointProcess (periodic, cc)", 75, 600)
            jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
            return float(jitter * 100)
        except:
            return 1.0
    
    def _get_shimmer(self, sound):
        """Voice quality (higher = more strained)."""
        try:
            point_process = call(sound, "To PointProcess (periodic, cc)", 75, 600)
            shimmer = call([sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            return float(shimmer * 100)
        except:
            return 3.0
    
    def _get_speaking_rate(self, audio, sr):
        """Estimate words per minute."""
        # Detect syllables via energy peaks
        energy = librosa.feature.rms(y=audio)[0]
        peaks = librosa.util.peak_pick(energy, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.1, wait=10)
        
        duration = len(audio) / sr
        syllables_per_sec = len(peaks) / duration
        words_per_min = (syllables_per_sec / 1.5) * 60
        
        return float(words_per_min)
    
    def _get_energy(self, audio):
        """Voice loudness/intensity."""
        rms = librosa.feature.rms(y=audio)[0]
        return {
            'mean': float(np.mean(rms)),
            'std': float(np.std(rms))
        }
    
    def _calculate_mood(self, features):
        """
        Convert features to mood score (1-10).
        
        Logic:
        - High energy + normal pitch = positive (7-9)
        - Low energy + slow rate = low mood (2-4)
        - Normal everything = neutral (5-6)
        """
        pitch_mean = features['pitch']['mean']
        energy_mean = features['energy']['mean']
        speaking_rate = features['speaking_rate']
        jitter = features['jitter']
        
        # Energy score (most important indicator)
        energy_score = min(10, max(1, energy_mean * 1000))
        
        # Speaking rate score
        if speaking_rate < 80:
            rate_score = 3  # Very slow = depressed
        elif speaking_rate < 120:
            rate_score = 5
        elif speaking_rate < 160:
            rate_score = 7  # Normal
        elif speaking_rate < 200:
            rate_score = 8  # Energetic
        else:
            rate_score = 6  # Too fast = anxious
        
        # Pitch score
        if pitch_mean > 0:
            pitch_score = min(10, max(1, (pitch_mean - 100) / 15))
        else:
            pitch_score = 5
        
        # Voice quality penalty
        quality_penalty = min(3, (jitter + features['shimmer']) / 2)
        quality_score = max(1, 10 - quality_penalty)
        
        # Weighted combination
        final_score = (
            energy_score * 0.35 +
            rate_score * 0.25 +
            pitch_score * 0.20 +
            quality_score * 0.20
        )
        
        return max(1.0, min(10.0, final_score))
    
    def _calculate_confidence(self, features):
        """How confident are we in this analysis?"""
        confidence = 1.0
        
        # No pitch detected
        if features['pitch']['mean'] == 0:
            confidence *= 0.5
        
        # Poor audio quality
        if features['jitter'] > 5 or features['shimmer'] > 8:
            confidence *= 0.6
        
        # Unrealistic speaking rate
        if features['speaking_rate'] < 40 or features['speaking_rate'] > 250:
            confidence *= 0.7
        
        return max(0.1, min(1.0, confidence))