# =============================================================================
# llm/decision_maker.py
# LLM generates final recommendations based on full mood analysis
# =============================================================================

from llm.llm_client import get_llm_client
from config import Config


class DecisionMaker:
    """
    Analyzes complete conversation and mood data to provide:
    1. Mood assessment summary
    2. Personalized recommendations
    3. Action steps user should take
    
    This is the FINAL output after analyzing voice + text responses.
    """
    
    def __init__(self):
        Config.validate()
        self.llm_client = get_llm_client()
        self.model = Config.LLM_MODEL
    
    def generate_recommendation(self, mood_data: dict, 
                               user_responses: dict,
                               conversation_history: list) -> dict:
        """
        Generate comprehensive recommendation based on all data.
        
        Args:
            mood_data: Aggregated mood scores
            user_responses: What user said (text + voice analysis)
            conversation_history: Previous interactions
            
        Returns:
            {
                'summary': str,           # Mood assessment
                'recommendations': list,  # What to do
                'urgency': str,          # low/medium/high
                'supportSuggestions': list
            }
        """
        
        print("\n🧠 GENERATING FINAL RECOMMENDATIONS...")
        
        # Build comprehensive context
        context = self._build_full_context(mood_data, user_responses, conversation_history)
        
        # Get system prompt based on mood severity
        system_prompt = self._get_decision_system_prompt(mood_data['category'])
        
        user_prompt = f"""{context}

Based on this complete analysis, provide:

1. MOOD SUMMARY: A brief, empathetic summary of their current state (2-3 sentences)

2. RECOMMENDATIONS: 3-5 specific, actionable things they should do based on their mood:
   - Immediate actions (today)
   - Short-term steps (this week)
   - When to seek additional support

3. POSITIVE REINFORCEMENT: What they're doing well (if anything)

Format your response clearly with these sections."""

        try:
            response = self.llm_client.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            
            decision_text = response  # response is already a string
            
            # Parse into structured format
            result = self._parse_decision(decision_text, mood_data)
            
            print(f"\n{'='*70}")
            print("📋 FINAL ASSESSMENT & RECOMMENDATIONS")
            print(f"{'='*70}")
            print(f"\n{result['summary']}\n")
            print("WHAT YOU SHOULD DO:")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"  {i}. {rec}")
            
            if result.get('supportSuggestions'):
                print("\nADDITIONAL SUPPORT:")
                for sugg in result['supportSuggestions']:
                    print(f"  • {sugg}")
            
            print(f"\n{'='*70}\n")
            
            return result
            
        except Exception as e:
            print(f"⚠️ LLM error: {e}")
            return self._fallback_decision(mood_data)
    
    def _build_full_context(self, mood_data: dict, user_responses: dict, 
                           history: list) -> str:
        """Build comprehensive context for decision making."""
        
        context = f"""COMPLETE MOOD ANALYSIS:

Overall Mood Score: {mood_data['overallMood']}/10
Category: {mood_data['category']}

Component Breakdown:
- Voice Analysis: {mood_data.get('voiceComponent', 'N/A')}/10
  Voice features: {user_responses.get('voice_features', 'N/A')}
- Text Sentiment: {mood_data.get('textComponent', 'N/A')}/10
  Text indicators: {user_responses.get('text_indicators', 'N/A')}
"""
        
        if mood_data.get('discrepancy'):
            context += f"\n🚨 DISCREPANCY DETECTED:\n{mood_data['discrepancy']['interpretation']}\n"
        
        context += f"\nWHAT USER SAID:\n\"{user_responses.get('text', '')}\"\n"
        
        if history and len(history) > 1:
            context += f"\nMOOD TREND (last {len(history)} interactions):\n"
            for h in history:
                context += f"- {h['timestamp'][:10]}: {h['mood']:.1f}/10 ({h['category']})\n"
            
            # Add trend analysis
            moods = [h['mood'] for h in history]
            if moods[-1] > moods[0] + 2:
                context += "\n📈 Mood has been IMPROVING over time\n"
            elif moods[-1] < moods[0] - 2:
                context += "\n📉 Mood has been DECLINING over time - ATTENTION NEEDED\n"
        
        return context
    
    def _get_decision_system_prompt(self, category: str) -> str:
        """Get system prompt for decision making."""
        
        base = """You are a mental health-aware AI advisor. Provide practical, 
evidence-based recommendations tailored to the user's mood and situation.

Your recommendations should be:
- Specific and actionable
- Appropriate for their emotional state
- Balanced (not too overwhelming)
- Empowering (help them take control)
"""
        
        additions = {
            'very_low': """
CRITICAL: User is in significant distress. Your recommendations MUST:
- Prioritize immediate safety and support
- Suggest professional help (therapist, crisis line)
- Provide concrete coping strategies
- Be gentle but direct about severity""",

            'low': """
User is struggling but stable. Your recommendations should:
- Validate their difficulty
- Suggest self-care and coping strategies
- Encourage connection with support system
- Recommend professional help if pattern continues""",

            'neutral': """
User is stable. Your recommendations should:
- Help maintain balance
- Suggest proactive wellness habits
- Support decision-making
- Encourage planning for challenges""",

            'positive': """
User is doing well. Your recommendations should:
- Reinforce what's working
- Help sustain positive momentum
- Suggest ways to build resilience
- Encourage goal pursuit""",

            'very_positive': """
User is very energized. Your recommendations should:
- Celebrate their state
- Help channel energy productively
- Gently ensure basics are covered (sleep, eating)
- Watch for potential mania if extreme"""
        }
        
        return base + additions.get(category, additions['neutral'])
    
    def _parse_decision(self, decision_text: str, mood_data: dict) -> dict:
        """Parse LLM output into structured format."""
        
        # Simple parsing - split by sections
        lines = decision_text.split('\n')
        
        summary = []
        recommendations = []
        support = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            lower = line.lower()
            if 'summary' in lower or 'assessment' in lower:
                current_section = 'summary'
            elif 'recommendation' in lower or 'what' in lower and 'do' in lower:
                current_section = 'recommendations'
            elif 'support' in lower or 'help' in lower:
                current_section = 'support'
            elif current_section == 'summary':
                summary.append(line)
            elif current_section == 'recommendations':
                if line[0].isdigit() or line.startswith('-') or line.startswith('•'):
                    recommendations.append(line.lstrip('0123456789.-• '))
            elif current_section == 'support':
                if line.startswith('-') or line.startswith('•'):
                    support.append(line.lstrip('-• '))
        
        # Determine urgency
        mood = mood_data['overallMood']
        if mood < 3:
            urgency = 'high'
        elif mood < 5:
            urgency = 'medium'
        else:
            urgency = 'low'
        
        return {
            'summary': ' '.join(summary) if summary else decision_text[:200],
            'recommendations': recommendations if recommendations else [decision_text],
            'urgency': urgency,
            'supportSuggestions': support,
            'fullText': decision_text
        }
    
    def _fallback_decision(self, mood_data: dict) -> dict:
        """Fallback recommendations if LLM fails."""
        
        category = mood_data['category']
        mood = mood_data['overallMood']
        
        templates = {
            'very_low': {
                'summary': f"Your mood is very low ({mood}/10). This indicates significant distress that needs immediate attention.",
                'recommendations': [
                    "If you're having thoughts of self-harm, call 988 (Suicide & Crisis Lifeline) immediately",
                    "Reach out to a trusted friend or family member today",
                    "Schedule an appointment with a mental health professional this week",
                    "Practice basic self-care: eat something, drink water, try to rest",
                    "Avoid making major decisions while in distress"
                ],
                'urgency': 'high',
                'supportSuggestions': [
                    "988 Suicide & Crisis Lifeline",
                    "Crisis Text Line: Text HOME to 741741"
                ]
            },
            'low': {
                'summary': f"Your mood is low ({mood}/10). You're struggling, which is completely valid.",
                'recommendations': [
                    "Practice gentle self-care: take a walk, listen to calming music",
                    "Connect with a friend or loved one, even briefly",
                    "Write down what's bothering you to process your feelings",
                    "Consider talking to a therapist if this persists",
                    "Avoid isolating yourself"
                ],
                'urgency': 'medium',
                'supportSuggestions': []
            },
            'neutral': {
                'summary': f"Your mood is stable ({mood}/10). This is a good baseline to work from.",
                'recommendations': [
                    "Maintain your current self-care routines",
                    "Plan something small to look forward to",
                    "Check in with yourself regularly",
                    "Address any lingering stressors proactively"
                ],
                'urgency': 'low',
                'supportSuggestions': []
            },
            'positive': {
                'summary': f"Your mood is positive ({mood}/10). You're doing well!",
                'recommendations': [
                    "Identify what's contributing to feeling good",
                    "Build on this momentum with meaningful activities",
                    "Help others or give back in some way",
                    "Plan for challenges to maintain resilience"
                ],
                'urgency': 'low',
                'supportSuggestions': []
            },
            'very_positive': {
                'summary': f"Your mood is very high ({mood}/10). You're feeling great!",
                'recommendations': [
                    "Channel this energy into productive projects",
                    "Make sure you're still sleeping and eating well",
                    "Avoid impulsive major decisions",
                    "Share your positive energy with others"
                ],
                'urgency': 'low',
                'supportSuggestions': []
            }
        }
        
        return templates.get(category, templates['neutral'])