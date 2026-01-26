# =============================================================================
# services/adaptive_analyzer.py
# Adaptive mood analysis using LLM reasoning instead of fixed rules
# =============================================================================

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from llm.llm_client import LLMClient


class AdaptiveMoodAnalyzer:
    """
    LLM-driven adaptive mood analysis system.
    
    Replaces hard-coded rules with intelligent reasoning:
    - Dynamic analysis windows (not fixed 6-day or any fixed period)
    - Context-aware mood interpretation
    - Adaptive intervention timing
    - Personalized insights based on patterns
    """
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def analyze_mood_history(self, mood_entries: List[Dict]) -> Dict:
        """
        Analyze mood history with adaptive time windows.
        
        Args:
            mood_entries: List of mood entries with:
                - timestamp
                - moodScore
                - emotionalTone
                - transcription (if voice)
                - content (if text)
        
        Returns:
            {
                'analysisWindow': str,  # "last 3 days", "past week", etc.
                'trendDirection': str,  # improving, declining, stable, volatile
                'emotionalPattern': str,  # Detected patterns
                'needsAttention': bool,  # Whether intervention is needed
                'interventionReason': str,  # Why intervention is suggested
                'supportLevel': str,  # none, gentle, moderate, urgent
                'insights': str,  # LLM-generated insights
                'recommendations': List[str]  # Actionable suggestions
            }
        """
        if not mood_entries:
            return self._empty_analysis()
        
        # Let LLM decide analysis window based on data density and patterns
        analysis_window = self._determine_analysis_window(mood_entries)
        
        # Filter entries within the adaptive window
        relevant_entries = self._filter_entries_by_window(mood_entries, analysis_window)
        
        # Use LLM to analyze patterns
        analysis = self._llm_analyze_patterns(relevant_entries, analysis_window)
        
        return analysis
    
    def _determine_analysis_window(self, mood_entries: List[Dict]) -> Dict:
        """
        Let LLM decide the optimal analysis window based on data characteristics.
        """
        if len(mood_entries) == 0:
            return {'days': 7, 'reason': 'default'}
        
        # Calculate data density and recency
        now = datetime.now()
        timestamps = [datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')) 
                     for e in mood_entries]
        
        days_covered = (now - min(timestamps)).days + 1
        entries_per_day = len(mood_entries) / max(1, days_covered)
        
        # Calculate mood volatility
        scores = [e.get('moodScore', 5) for e in mood_entries]
        volatility = self._calculate_volatility(scores)
        
        try:
            prompt = f"""Determine the optimal time window for mood analysis given these characteristics:

DATA CHARACTERISTICS:
- Total entries: {len(mood_entries)}
- Time span: {days_covered} days
- Entry frequency: {entries_per_day:.1f} entries/day
- Mood volatility: {volatility:.2f} (0=stable, 1=very volatile)
- Most recent entry: {timestamps[0] if timestamps else 'None'}

GUIDELINES:
- For stable moods + sparse data → analyze longer window (7-14 days)
- For volatile moods → focus on recent data (2-5 days)
- For high-frequency entries → shorter window suffices (3-7 days)
- For concerning patterns → prioritize most recent (1-3 days)

Respond in JSON format:
{{
    "days": integer (1-30),
    "reason": "Brief explanation of why this window size"
}}"""
            
            response = self.llm_client.generate(prompt, max_tokens=150)
            
            import json
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0].strip()
            elif '```' in response:
                response = response.split('```')[1].split('```')[0].strip()
            
            result = json.loads(response)
            return result
            
        except Exception as e:
            print(f"Window determination failed, using default: {e}")
            # Fallback logic
            if volatility > 0.3:
                return {'days': 3, 'reason': 'high volatility detected'}
            elif entries_per_day > 2:
                return {'days': 5, 'reason': 'frequent entries'}
            else:
                return {'days': 7, 'reason': 'default window'}
    
    def _filter_entries_by_window(self, entries: List[Dict], window: Dict) -> List[Dict]:
        """Filter entries within the analysis window."""
        days = window.get('days', 7)
        cutoff = datetime.now() - timedelta(days=days)
        
        filtered = []
        for entry in entries:
            try:
                timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                if timestamp >= cutoff:
                    filtered.append(entry)
            except:
                continue
        
        return filtered
    
    def _llm_analyze_patterns(self, entries: List[Dict], window: Dict) -> Dict:
        """Use LLM to analyze mood patterns without hard-coded rules."""
        
        if not entries:
            return self._empty_analysis()
        
        # Prepare data summary for LLM
        entries_summary = self._summarize_entries_for_llm(entries)
        
        try:
            prompt = f"""Analyze this person's emotional wellbeing based on their recent mood entries.

ANALYSIS WINDOW: Past {window['days']} days
TOTAL ENTRIES: {len(entries)}

MOOD ENTRIES:
{entries_summary}

ANALYSIS REQUIRED:
1. **Trend Direction**: Is mood improving, declining, stable, or volatile?
2. **Emotional Patterns**: What recurring themes or emotions are present?
3. **Needs Attention**: Does this person need support? Consider:
   - Persistent low mood (not just one bad day)
   - Emotional discrepancies (saying "fine" but voice shows distress)
   - Signs of isolation, fatigue, hopelessness
   - Sudden emotional shifts
4. **Support Level**: none, gentle (encouragement), moderate (resources), urgent (professional help)
5. **Personalized Insights**: What's the overall emotional story?
6. **Actionable Recommendations**: What would genuinely help this person?

IMPORTANT: Be empathetic, not clinical. Avoid forcing timelines or streaks.

Respond in JSON:
{{
    "trendDirection": "improving|declining|stable|volatile",
    "emotionalPattern": "Brief description of patterns",
    "needsAttention": true|false,
    "interventionReason": "Why or why not",
    "supportLevel": "none|gentle|moderate|urgent",
    "insights": "2-3 sentence human-friendly analysis",
    "recommendations": ["action1", "action2", "action3"]
}}"""
            
            response = self.llm_client.generate(prompt, max_tokens=500)
            
            import json
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0].strip()
            elif '```' in response:
                response = response.split('```')[1].split('```')[0].strip()
            
            analysis = json.loads(response)
            analysis['analysisWindow'] = f"past {window['days']} days"
            
            return analysis
            
        except Exception as e:
            print(f"LLM pattern analysis failed: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_analysis(entries, window)
    
    def _summarize_entries_for_llm(self, entries: List[Dict]) -> str:
        """Create a concise summary of mood entries for LLM."""
        lines = []
        
        for i, entry in enumerate(entries[:20], 1):  # Limit to 20 most recent
            timestamp = entry.get('timestamp', 'Unknown')
            mood_score = entry.get('moodScore', 'N/A')
            emotional_tone = entry.get('emotionalTone', {})
            primary_emotion = emotional_tone.get('primary', 'neutral') if isinstance(emotional_tone, dict) else 'neutral'
            
            # Get content (voice transcription or text)
            content = entry.get('transcription', entry.get('content', ''))[:100]
            
            lines.append(f"{i}. [{timestamp}] Mood: {mood_score}/10, Emotion: {primary_emotion}")
            if content:
                lines.append(f"   Said: \"{content}...\"")
        
        return '\n'.join(lines)
    
    def _calculate_volatility(self, scores: List[float]) -> float:
        """Calculate mood volatility (0=stable, 1=very volatile)."""
        if len(scores) < 2:
            return 0.0
        
        # Calculate standard deviation normalized to 0-1
        import statistics
        try:
            std_dev = statistics.stdev(scores)
            # Mood range is 1-10, so std_dev of 4.5 would be max (perfect volatility)
            volatility = min(1.0, std_dev / 4.5)
            return volatility
        except:
            return 0.0
    
    def _empty_analysis(self) -> Dict:
        """Return analysis for when there's no data."""
        return {
            'analysisWindow': 'no data',
            'trendDirection': 'unknown',
            'emotionalPattern': 'No mood entries yet',
            'needsAttention': False,
            'interventionReason': 'Insufficient data',
            'supportLevel': 'none',
            'insights': 'Start recording your moods to receive personalized insights.',
            'recommendations': ['Record your first mood entry', 'Try voice recording for better insights']
        }
    
    def _fallback_analysis(self, entries: List[Dict], window: Dict) -> Dict:
        """Fallback analysis if LLM fails."""
        scores = [e.get('moodScore', 5) for e in entries]
        avg_score = sum(scores) / len(scores) if scores else 5
        
        # Simple trend detection
        recent_avg = sum(scores[:3]) / 3 if len(scores) >= 3 else avg_score
        older_avg = sum(scores[3:6]) / 3 if len(scores) >= 6 else avg_score
        
        if recent_avg > older_avg + 1:
            trend = 'improving'
        elif recent_avg < older_avg - 1:
            trend = 'declining'
        else:
            trend = 'stable'
        
        needs_attention = avg_score < 4 or (trend == 'declining' and avg_score < 5.5)
        
        return {
            'analysisWindow': f"past {window['days']} days",
            'trendDirection': trend,
            'emotionalPattern': f"Average mood: {avg_score:.1f}/10",
            'needsAttention': needs_attention,
            'interventionReason': 'Mood appears low' if needs_attention else 'Mood seems acceptable',
            'supportLevel': 'moderate' if needs_attention else 'none',
            'insights': f"Your mood has been {trend} recently with an average of {avg_score:.1f}/10.",
            'recommendations': ['Continue tracking your mood', 'Consider talking to someone']
        }
