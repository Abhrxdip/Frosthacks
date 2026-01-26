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