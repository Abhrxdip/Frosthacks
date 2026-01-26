# =============================================================================
# llm/question_generator.py
# LLM generates personalized questions based on mood
# =============================================================================

from llm.llm_client import get_llm_client
from config import Config


class QuestionGenerator:
    """
    Uses LLM to generate personalized questions based on user's mood.
    
    The questions will prompt the user to:
    1. Reflect on their day (past)
    2. Express current feelings (present)
    3. Think about decisions (future)
    
    Then user answers via text + voice, which gets analyzed.
    """
    
    def __init__(self):
        Config.validate()
        self.llm_client = get_llm_client()  
        self.model = Config.LLM_MODEL
    
    def generate_initial_questions(self) -> str:
        """
        Generate opening questions to start conversation.
        
        These are general questions to get the user talking,
        which will then be analyzed for mood.
        """
        
        system_prompt = """You are a warm, empathetic AI companion designed to help people 
reflect on their day and feelings. 

Generate 2-3 thoughtful questions that encourage the user to open up about:
1. How their day went
2. How they're currently feeling
3. What's on their mind

Keep questions warm, conversational, and open-ended. Make the user feel comfortable sharing."""

        user_prompt = """Generate opening questions for a daily check-in conversation. 
The user will answer via voice and text, which will be analyzed to understand their mood.

Format: Just return the questions naturally, one after another."""

        try:
            # Use the provider-specific wrapper method
            questions = self.llm_client.generate(system_prompt=system_prompt, user_prompt=user_prompt)
            
            print(f"\n🤖 LLM INITIAL QUESTIONS:\n{questions}\n")
            return questions
            
        except Exception as e:
            print(f"⚠️ LLM error: {e}")
            # Fallback questions
            return """How was your day today? What's been on your mind lately? 
How are you feeling right now?"""
    
    def generate_followup_questions(self, mood_data: dict, 
                                   conversation_history: list) -> str:
        """
        Generate follow-up questions based on detected mood and history.
        
        Args:
            mood_data: Aggregated mood analysis
            conversation_history: Previous interactions
            
        Returns:
            Personalized follow-up questions
        """
        
        category = mood_data['category']
        overall_mood = mood_data['overallMood']
        
        # Get appropriate system prompt for mood
        system_prompt = self._get_system_prompt_for_mood(category)
        
        # Build context
        context = self._build_context(mood_data, conversation_history)
        
        user_prompt = f"""{context}

Based on this mood analysis, generate 2-3 thoughtful follow-up questions that:
1. Show you understand their emotional state
2. Help them explore what's contributing to their mood
3. Guide them toward reflection or planning

Be warm and conversational."""

        try:
            questions = self.llm_client.generate(system_prompt=system_prompt, user_prompt=user_prompt)
            
            print(f"\n🤖 LLM FOLLOW-UP QUESTIONS:\n{questions}\n")
            return questions
            
        except Exception as e:
            print(f"⚠️ LLM error: {e}")
            return self._fallback_questions(category)
    
    def _get_system_prompt_for_mood(self, category: str) -> str:
        """Get mood-appropriate system prompt."""
        
        prompts = {
            'very_low': """You are a compassionate crisis supporter. The user is in significant distress.
Your role is to:
- Acknowledge their pain without minimizing
- Check if they're safe and have support
- Ask gentle questions about what might help
- Be direct, warm, and non-judgmental""",

            'low': """You are an empathetic listener. The user is struggling or feeling down.
Your role is to:
- Validate their difficult feelings
- Help them explore what's contributing
- Gently suggest coping strategies
- Ask about small, achievable next steps""",

            'neutral': """You are a reflective companion. The user's mood is stable.
Your role is to:
- Help them explore their day and thoughts
- Support decision-making if needed
- Encourage forward planning
- Be conversational and curious""",

            'positive': """You are an encouraging supporter. The user is doing well.
Your role is to:
- Celebrate what's going right
- Help them identify what's working
- Support building on positive momentum
- Be energized and optimistic""",

            'very_positive': """You are an enthusiastic companion. The user is very upbeat.
Your role is to:
- Match their positive energy
- Help channel excitement productively
- Support ambitious planning
- Gently ensure they're taking care of basics too"""
        }
        
        return prompts.get(category, prompts['neutral'])
    
    def _build_context(self, mood_data: dict, history: list) -> str:
        """Build context string for LLM."""
        
        from datetime import datetime
        hour = datetime.now().hour
        time_context = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"
        
        context = f"""Current Context:
Time: {time_context}
Overall Mood: {mood_data['overallMood']}/10 ({mood_data['category']})
Voice Mood: {mood_data.get('voiceComponent', 'N/A')}/10
Text Mood: {mood_data.get('textComponent', 'N/A')}/10
"""
        
        if mood_data.get('discrepancy'):
            context += f"\n⚠️ Note: {mood_data['discrepancy']['interpretation']}\n"
        
        if history and len(history) > 1:
            context += "\nRecent mood trend:\n"
            for h in history[-3:]:
                context += f"- {h['category']}: \"{h.get('userText', '')[:60]}...\"\n"
        
        return context
    
    def _fallback_questions(self, category: str) -> str:
        """Template questions if LLM fails."""
        
        templates = {
            'very_low': "I can hear you're really struggling right now. Are you safe? Is there someone you can talk to? What's one small thing that might help in this moment?",
            
            'low': "It sounds like you're having a tough time. What's weighing most heavily on you? What usually helps when you feel this way?",
            
            'neutral': "How are you really feeling about your day? What's on your mind as you look ahead? Anything you're trying to decide?",
            
            'positive': "That's great to hear! What's been going particularly well? How can you keep this momentum going?",
            
            'very_positive': "You sound energized! What's fueling this great mood? What do you want to accomplish while feeling this good?"
        }
        
        return templates.get(category, templates['neutral'])