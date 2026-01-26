# =============================================================================
# services/mood_aggregator.py
# Combines voice + text mood scores
# =============================================================================

class MoodAggregator:
    """
    Combines voice and text mood scores into single assessment.
    
    Strategy:
    - Voice weighted 60% (harder to fake)
    - Text weighted 40% (can be controlled)
    - Detects discrepancies (masking emotions)
    """
    
    def aggregate(self, voice_score: float, text_score: float, 
                  voice_confidence: float = 1.0) -> dict:
        """
        Combine voice + text mood scores.
        
        Args:
            voice_score: Mood from voice (1-10)
            text_score: Mood from text (1-10)
            voice_confidence: How confident in voice analysis (0-1)
            
        Returns:
            {
                'overallMood': float,
                'category': str,
                'voiceComponent': float,
                'textComponent': float,
                'discrepancy': dict or None
            }
        """
        
        # Adjust voice weight based on confidence
        voice_weight = 0.6 * voice_confidence
        text_weight = 1 - voice_weight
        
        # Combined mood
        overall = (voice_score * voice_weight) + (text_score * text_weight)
        
        # Categorize mood
        category = self._categorize(overall)
        
        # Detect discrepancy
        discrepancy = None
        diff = abs(voice_score - text_score)
        if diff > 3:  # Significant difference
            discrepancy = {
                'detected': True,
                'difference': round(diff, 2),
                'interpretation': self._interpret_discrepancy(voice_score, text_score)
            }
        
        result = {
            'overallMood': round(overall, 2),
            'category': category,
            'voiceComponent': round(voice_score, 2),
            'textComponent': round(text_score, 2),
            'discrepancy': discrepancy
        }
        
        print(f"\n📊 MOOD AGGREGATION:")
        print(f"   Voice: {voice_score:.1f}/10")
        print(f"   Text: {text_score:.1f}/10")
        print(f"   Overall: {overall:.1f}/10 ({category})")
        if discrepancy:
            print(f"   ⚠️ {discrepancy['interpretation']}")
        
        return result
    
    def _categorize(self, score: float) -> str:
        """Convert numeric score to category."""
        if score < 3:
            return "very_low"
        elif score < 5:
            return "low"
        elif score < 7:
            return "neutral"
        elif score < 9:
            return "positive"
        else:
            return "very_positive"
    
    def _interpret_discrepancy(self, voice: float, text: float) -> str:
        """Explain why voice and text differ."""
        if text > voice + 3:
            return "Text more positive than voice - may be putting on brave face"
        else:
            return "Voice more positive than text - may be venting but actually coping"


# =============================================================================
# utils/session_manager.py
# Simple JSON-based session tracking
# =============================================================================

import json
import os
from datetime import datetime
from typing import Optional, List


class SessionManager:
    """
    Manages conversation history using simple JSON file.
    No database needed - just stores in data/sessions.json
    """
    
    def __init__(self, session_file="data/sessions.json"):
        self.session_file = session_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create sessions file if it doesn't exist."""
        os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
        if not os.path.exists(self.session_file):
            with open(self.session_file, 'w') as f:
                json.dump({"conversations": []}, f)
    
    def add_interaction(self, mood_data: dict, user_text: str, 
                       llm_questions: str, user_audio_path: Optional[str] = None):
        """
        Save interaction to history.
        
        Args:
            mood_data: Aggregated mood result
            user_text: What user said (text)
            llm_questions: Questions LLM asked
            user_audio_path: Path to user's audio (optional)
        """
        
        # Load existing
        with open(self.session_file, 'r') as f:
            data = json.load(f)
        
        # Add new interaction
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'mood': mood_data['overallMood'],
            'category': mood_data['category'],
            'voiceMood': mood_data.get('voiceComponent'),
            'textMood': mood_data.get('textComponent'),
            'userText': user_text[:200],  # Truncate for storage
            'llmQuestions': llm_questions,
            'audioPath': user_audio_path
        }
        
        data['conversations'].append(interaction)
        
        # Keep only last 10 interactions
        data['conversations'] = data['conversations'][-10:]
        
        # Save
        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_final_decision(self, decision: str):
        """Add LLM's final recommendation to last interaction."""
        with open(self.session_file, 'r') as f:
            data = json.load(f)
        
        if data['conversations']:
            data['conversations'][-1]['llmDecision'] = decision
        
        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_recent_history(self, n: int = 5) -> List[dict]:
        """Get last N conversations."""
        with open(self.session_file, 'r') as f:
            data = json.load(f)
        
        return data['conversations'][-n:]
    
    def get_mood_trend(self) -> dict:
        """Analyze mood trend over recent conversations."""
        history = self.get_recent_history(10)
        
        if len(history) < 2:
            return {'trend': 'insufficient_data'}
        
        moods = [h['mood'] for h in history]
        recent_avg = sum(moods[-3:]) / min(3, len(moods))
        early_avg = sum(moods[:3]) / min(3, len(moods))
        
        if recent_avg > early_avg + 1:
            direction = 'improving'
        elif recent_avg < early_avg - 1:
            direction = 'declining'
        else:
            direction = 'stable'
        
        return {
            'trend': direction,
            'averageMood': round(sum(moods) / len(moods), 2),
            'recentMood': round(recent_avg, 2),
            'count': len(moods)
        }
    
    def clear_history(self):
        """Clear all conversation history."""
        with open(self.session_file, 'w') as f:
            json.dump({"conversations": []}, f)
        print("🗑️ Conversation history cleared")