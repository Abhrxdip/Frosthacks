# =============================================================================
# services/sentiment_analyzer.py
# Analyzes text sentiment
# =============================================================================

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """
    Analyzes emotional tone in text.
    
    Uses VADER (Valence Aware Dictionary) which understands:
    - Punctuation: "Good!" vs "Good!!!"
    - Capitalization: "I'm ANGRY" vs "I'm angry"
    - Emoticons: :), :(, :D
    - Slang: "sux", "lol", "meh"
    """
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment from text.
        
        Args:
            text: User's text input
            
        Returns:
            {
                'moodScore': float (1-10),
                'sentiment': dict (VADER scores),
                'indicators': dict (emotional cues)
            }
        """
        print(f"💬 Analyzing text: '{text[:50]}...'")
        
        if not text or len(text.strip()) == 0:
            return {
                'moodScore': 5.0,
                'sentiment': {'compound': 0},
                'indicators': {}
            }
        
        # Get VADER sentiment scores
        scores = self.analyzer.polarity_scores(text)
        
        # Convert to 1-10 scale
        mood_score = self._convert_to_mood_score(scores['compound'])
        
        # Detect emotional indicators
        indicators = self._detect_indicators(text)
        
        print(f"   Text Mood: {mood_score}/10")
        
        return {
            'moodScore': round(mood_score, 2),
            'sentiment': scores,
            'indicators': indicators
        }
    
    def _convert_to_mood_score(self, compound: float) -> float:
        """
        Convert VADER compound score (-1 to +1) to mood (1 to 10).
        
        -1.0 → 1.0  (extremely negative)
        -0.5 → 3.0  (negative)
         0.0 → 5.5  (neutral)
        +0.5 → 8.0  (positive)
        +1.0 → 10.0 (extremely positive)
        """
        mood = (compound * 4.5) + 5.5
        return max(1.0, min(10.0, mood))
    
    def _detect_indicators(self, text: str) -> dict:
        """
        Detect emotional cues in text.
        
        Returns indicators like:
        - Has questions (uncertainty)
        - Has exclamations (intensity)
        - All caps (strong emotion)
        - Negative/positive words count
        """
        import re
        
        return {
            'hasQuestions': '?' in text,
            'hasExclamations': '!' in text,
            'hasAllCaps': bool(re.search(r'\b[A-Z]{3,}\b', text)),
            'negativeWords': self._count_negative_words(text),
            'positiveWords': self._count_positive_words(text),
            'length': len(text.split())
        }
    
    def _count_negative_words(self, text: str) -> int:
        """Count negative emotion keywords."""
        negative = [
            'sad', 'depressed', 'anxious', 'worried', 'stressed', 'upset',
            'angry', 'frustrated', 'tired', 'exhausted', 'overwhelmed',
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate',
            'lonely', 'hopeless', 'scared', 'afraid', 'nervous'
        ]
        text_lower = text.lower()
        return sum(1 for word in negative if word in text_lower)
    
    def _count_positive_words(self, text: str) -> int:
        """Count positive emotion keywords."""
        positive = [
            'happy', 'excited', 'great', 'good', 'excellent', 'amazing',
            'wonderful', 'fantastic', 'love', 'joy', 'grateful', 'thankful',
            'proud', 'confident', 'energized', 'motivated', 'hopeful',
            'peaceful', 'calm', 'relaxed', 'better', 'best'
        ]
        text_lower = text.lower()
        return sum(1 for word in positive if word in text_lower)