# =============================================================================
# services/voice_analyzer.py
# Analyzes voice emotion from audio file with speech-to-text and LLM analysis
# =============================================================================

import librosa
import numpy as np
import parselmouth
from parselmouth.praat import call
import warnings
import os
from typing import Optional
warnings.filterwarnings('ignore')

# Try to import speech recognition
try:
    import speech_recognition as sr
    HAS_SPEECH_RECOGNITION = True
except ImportError:
    HAS_SPEECH_RECOGNITION = False
    print("⚠️ speech_recognition not available. Install with: pip install SpeechRecognition")

# Import LLM client for emotional analysis
try:
    from llm.llm_client import LLMClient
    HAS_LLM = True
except ImportError:
    HAS_LLM = False


class VoiceAnalyzer:
    """
    Enhanced voice analyzer with speech-to-text and LLM emotional analysis.
    
    Features:
    - Acoustic analysis (pitch, jitter, shimmer, energy, speaking rate)
    - Speech-to-text transcription
    - LLM-based emotional tone detection (stress, anxiety, calm, sadness, etc.)
    - Natural language emotional summary
    - Confidence scoring
    """
    
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.llm_client = LLMClient() if HAS_LLM else None
        self.recognizer = sr.Recognizer() if HAS_SPEECH_RECOGNITION else None
    
    def analyze(self, audio_path: str, use_llm: bool = True) -> dict:
        """
        Comprehensive voice analysis with speech-to-text and LLM emotional insights.
        
        Args:
            audio_path: Path to audio file (WAV, MP3, WEBM, etc.)
            use_llm: Whether to use LLM for emotional analysis
            
        Returns:
            {
                'transcription': str,  # What was said
                'acousticFeatures': dict,  # Pitch, energy, jitter, etc.
                'emotionalTone': {  # LLM-detected emotions
                    'primary': str,  # Main emotion detected
                    'secondary': List[str],  # Additional emotions
                    'intensity': float  # 0-1 scale
                },
                'emotionalSummary': str,  # Natural language description
                'moodScore': float,  # Overall 1-10 score
                'confidence': float,  # 0-1 confidence
                'llmInsights': str  # Detailed LLM analysis
            }
        """
        print(f"🎤 Analyzing voice from: {audio_path}")
        
        try:
            # Step 1: Extract acoustic features
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            sound = parselmouth.Sound(audio_path)
            
            acoustic_features = {
                'pitch': self._get_pitch(sound),
                'jitter': self._get_jitter(sound),
                'shimmer': self._get_shimmer(sound),
                'speaking_rate': self._get_speaking_rate(audio, sr),
                'energy': self._get_energy(audio)
            }
            
            # Step 2: Speech-to-text transcription
            transcription = self._transcribe_audio(audio_path)
            
            # Step 3: Interpret acoustic features
            acoustic_interpretation = self._interpret_acoustic_features(acoustic_features)
            
            # Step 4: LLM emotional analysis
            llm_analysis = None
            emotional_summary = None
            emotional_tone = None
            
            if use_llm and self.llm_client and (transcription or acoustic_interpretation):
                llm_analysis = self._get_llm_emotional_analysis(
                    transcription, 
                    acoustic_features,
                    acoustic_interpretation
                )
                emotional_tone = llm_analysis.get('emotionalTone')
                emotional_summary = llm_analysis.get('summary')
            
            # Step 5: Calculate final mood score (adaptive, not hard-coded)
            if llm_analysis and 'moodScore' in llm_analysis:
                mood_score = llm_analysis['moodScore']
            else:
                mood_score = self._calculate_mood(acoustic_features)
            
            confidence = self._calculate_confidence(acoustic_features, transcription, llm_analysis)
            
            print(f"   📝 Transcription: {transcription[:50] if transcription else 'N/A'}...")
            print(f"   🎭 Emotional Tone: {emotional_tone.get('primary') if emotional_tone else 'N/A'}")
            print(f"   💯 Mood Score: {mood_score}/10 (confidence: {confidence:.2f})")
            
            return {
                'transcription': transcription or '',
                'acousticFeatures': acoustic_features,
                'acousticInterpretation': acoustic_interpretation,
                'emotionalTone': emotional_tone or {'primary': 'neutral', 'secondary': [], 'intensity': 0.5},
                'emotionalSummary': emotional_summary or self._generate_fallback_summary(acoustic_features),
                'moodScore': round(mood_score, 2),
                'confidence': round(confidence, 2),
                'llmInsights': llm_analysis.get('insights') if llm_analysis else None
            }
            
        except Exception as e:
            print(f"   ⚠️ Voice analysis failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'transcription': '',
                'acousticFeatures': {},
                'emotionalTone': {'primary': 'unknown', 'secondary': [], 'intensity': 0},
                'emotionalSummary': 'Unable to analyze voice recording.',
                'moodScore': 5.0,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _transcribe_audio(self, audio_path: str) -> Optional[str]:
        """Convert speech to text using Google Speech Recognition."""
        if not HAS_SPEECH_RECOGNITION or not self.recognizer:
            return None
        
        try:
            # Convert to WAV if needed
            import subprocess
            wav_path = audio_path.replace('.webm', '.wav').replace('.mp3', '.wav')
            
            if not audio_path.endswith('.wav'):
                # Use ffmpeg if available
                try:
                    subprocess.run(['ffmpeg', '-i', audio_path, '-ar', '16000', wav_path], 
                                 capture_output=True, check=True)
                except:
                    wav_path = audio_path  # Fallback to original
            
            with sr.AudioFile(wav_path if os.path.exists(wav_path) else audio_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                
                # Clean up temporary WAV file
                if wav_path != audio_path and os.path.exists(wav_path):
                    os.unlink(wav_path)
                
                return text
        except Exception as e:
            print(f"   Speech-to-text failed: {e}")
            return None
    
    def _interpret_acoustic_features(self, features: dict) -> dict:
        """Interpret acoustic features in human terms."""
        pitch_mean = features['pitch']['mean']
        energy_mean = features['energy']['mean']
        speaking_rate = features['speaking_rate']
        jitter = features['jitter']
        shimmer = features['shimmer']
        
        interpretation = {
            'arousal': 'neutral',
            'stress_level': 'moderate',
            'voice_quality': 'normal',
            'speaking_pace': 'normal',
            'energy_level': 'moderate'
        }
        
        # Interpret arousal (high pitch = high arousal)
        if pitch_mean > 200:
            interpretation['arousal'] = 'high'
        elif pitch_mean > 150:
            interpretation['arousal'] = 'moderate'
        elif pitch_mean > 0:
            interpretation['arousal'] = 'low'
        
        # Interpret stress (high jitter = stress/anxiety)
        if jitter > 3:
            interpretation['stress_level'] = 'high'
        elif jitter > 1.5:
            interpretation['stress_level'] = 'moderate'
        else:
            interpretation['stress_level'] = 'low'
        
        # Interpret voice quality
        if shimmer > 6 or jitter > 4:
            interpretation['voice_quality'] = 'strained'
        elif shimmer < 3 and jitter < 1.5:
            interpretation['voice_quality'] = 'clear'
        
        # Interpret speaking pace
        if speaking_rate < 80:
            interpretation['speaking_pace'] = 'very slow'
        elif speaking_rate < 120:
            interpretation['speaking_pace'] = 'slow'
        elif speaking_rate < 160:
            interpretation['speaking_pace'] = 'normal'
        elif speaking_rate < 200:
            interpretation['speaking_pace'] = 'fast'
        else:
            interpretation['speaking_pace'] = 'very fast'
        
        # Interpret energy
        if energy_mean > 0.015:
            interpretation['energy_level'] = 'high'
        elif energy_mean > 0.008:
            interpretation['energy_level'] = 'moderate'
        else:
            interpretation['energy_level'] = 'low'
        
        return interpretation
    
    def _get_llm_emotional_analysis(self, transcription: str, acoustic_features: dict, 
                                    acoustic_interpretation: dict) -> Optional[dict]:
        """Use LLM to analyze emotional state from voice data."""
        if not self.llm_client:
            return None
        
        try:
            prompt = f"""Analyze the emotional state from this voice recording data:

SPOKEN WORDS: "{transcription or 'Not transcribed'}"

VOICE CHARACTERISTICS:
- Arousal level: {acoustic_interpretation.get('arousal')}
- Stress indicators: {acoustic_interpretation.get('stress_level')} stress
- Voice quality: {acoustic_interpretation.get('voice_quality')}
- Speaking pace: {acoustic_interpretation.get('speaking_pace')}
- Energy level: {acoustic_interpretation.get('energy_level')}

ACOUSTIC DETAILS:
- Pitch: {acoustic_features['pitch']['mean']:.1f} Hz
- Jitter: {acoustic_features['jitter']:.2f}%
- Speaking rate: {acoustic_features['speaking_rate']:.0f} wpm

Provide a comprehensive emotional analysis including:
1. Primary emotion detected (anxiety, stress, sadness, calm, contentment, excitement, fatigue, etc.)
2. Secondary emotions if present
3. Emotional intensity (0-1 scale)
4. A natural language summary (1-2 sentences) of how the person sounds emotionally
5. Overall mood score (1-10 scale)
6. Key emotional insights

Format as JSON:
{{
    "emotionalTone": {{
        "primary": "emotion",
        "secondary": ["emotion1", "emotion2"],
        "intensity": 0.0-1.0
    }},
    "summary": "Natural language description",
    "moodScore": 1-10,
    "insights": "Detailed analysis"
}}"""
            
            response = self.llm_client.generate(prompt, max_tokens=400)
            
            # Parse JSON response
            import json
            # Extract JSON from markdown code blocks if present
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0].strip()
            elif '```' in response:
                response = response.split('```')[1].split('```')[0].strip()
            
            return json.loads(response)
            
        except Exception as e:
            print(f"   LLM emotional analysis failed: {e}")
            return None
    
    def _generate_fallback_summary(self, acoustic_features: dict) -> str:
        """Generate a simple emotional summary without LLM."""
        energy = acoustic_features['energy']['mean']
        rate = acoustic_features['speaking_rate']
        
        if energy < 0.008 and rate < 100:
            return "You sound low in energy and speaking slowly, possibly feeling fatigued or down."
        elif energy > 0.015 and rate > 160:
            return "You sound energetic and speaking quickly, possibly feeling excited or anxious."
        elif acoustic_features['jitter'] > 3:
            return "Your voice shows signs of tension or stress."
        else:
            return "Your emotional state appears relatively neutral."
    
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
    
    def _calculate_confidence(self, features, transcription=None, llm_analysis=None):
        """How confident are we in this analysis?"""
        confidence = 1.0
        
        # No pitch detected
        if features.get('pitch', {}).get('mean', 0) == 0:
            confidence *= 0.5
        
        # Poor audio quality
        jitter = features.get('jitter', 1)
        shimmer = features.get('shimmer', 3)
        if jitter > 5 or shimmer > 8:
            confidence *= 0.6
        
        # Unrealistic speaking rate
        rate = features.get('speaking_rate', 120)
        if rate < 40 or rate > 250:
            confidence *= 0.7
        
        # Boost confidence if we have transcription
        if transcription:
            confidence *= 1.1
        
        # Boost confidence if LLM analysis succeeded
        if llm_analysis:
            confidence *= 1.15
        
        return max(0.1, min(1.0, confidence))