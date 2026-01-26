# =============================================================================
# main.py
# Main application - orchestrates entire mood analysis flow
# =============================================================================

import os
import sys
from datetime import datetime

# Import all components
from config import Config
from services.voice_analyzer import VoiceAnalyzer
from services.sentiment_analyzer import SentimentAnalyzer
from services.aggregator import MoodAggregator
from llm.question_generator import QuestionGenerator
from llm.decision_maker import DecisionMaker
from utils.session_manager import SessionManager

# Optional imports (may not be installed)
try:
    import sounddevice as sd
    import soundfile as sf
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False


class MoodAnalysisApp:
    """
    Complete Mood Analysis Application
    
    Flow:
    1. LLM generates opening questions
    2. User answers via text + voice
    3. Analyze voice mood
    4. Analyze text sentiment
    5. Aggregate both scores
    6. Save to session history
    7. LLM generates final recommendations
    """
    
    def __init__(self):
        print("🚀 Initializing Mood Analysis System...")
        
        # Initialize all components
        self.voice_analyzer = VoiceAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.mood_aggregator = MoodAggregator()
        self.question_generator = QuestionGenerator()
        self.decision_maker = DecisionMaker()
        self.session_manager = SessionManager()
        
        print("✅ All systems ready!\n")
    
    def run(self):
        """Main application loop."""
        
        print("=" * 70)
        print("                    MOOD ANALYSIS SYSTEM")
        print("=" * 70)
        print("\nThis system will help you understand your emotional state and")
        print("provide personalized recommendations.\n")
        
        # Show menu
        print("OPTIONS:")
        print("1. Start new conversation")
        print("2. View conversation history")
        print("3. Clear history")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            self.start_conversation()
        elif choice == '2':
            self.view_history()
        elif choice == '3':
            self.session_manager.clear_history()
        elif choice == '4':
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")
            self.run()
    
    def start_conversation(self):
        """Start new conversation flow."""
        
        print("\n" + "=" * 70)
        print("STARTING NEW CONVERSATION")
        print("=" * 70 + "\n")
        
        # STEP 1: LLM generates opening questions
        print("🤖 AI is preparing questions for you...\n")
        questions = self.question_generator.generate_initial_questions()
        
        print(f"AI: {questions}\n")
        
        # STEP 2: Get user's response
        print("Please answer the questions above:")
        print("(You can provide both text and voice, or just text)\n")
        
        user_text = input("💬 Your text answer: ").strip()
        
        audio_path = None
        use_voice = input("\n🎙️ Do you want to record voice? (y/n): ").strip().lower()
        
        if use_voice == 'y':
            audio_path = self.get_voice_input()
        
        if not user_text and not audio_path:
            print("⚠️ No input provided. Returning to menu.")
            return self.run()
        
        # STEP 3: Analyze mood
        print("\n" + "-" * 70)
        print("ANALYZING YOUR MOOD...")
        print("-" * 70)
        
        mood_result = self.analyze_mood(user_text, audio_path)
        
        # STEP 4: Save to history
        self.session_manager.add_interaction(
            mood_data=mood_result['aggregated'],
            user_text=user_text,
            llm_questions=questions,
            user_audio_path=audio_path
        )
        
        # STEP 5: Get conversation history
        history = self.session_manager.get_recent_history()
        trend = self.session_manager.get_mood_trend()
        
        if trend['trend'] != 'insufficient_data':
            print(f"\n📈 MOOD TREND: {trend['trend']} (avg: {trend['averageMood']}/10)")
        
        # STEP 6: Generate final recommendations
        decision = self.decision_maker.generate_recommendation(
            mood_data=mood_result['aggregated'],
            user_responses={
                'text': user_text,
                # guard against None when voice/text analyses are missing
                'voice_features': (mood_result.get('voice') or {}).get('features'),
                'text_indicators': (mood_result.get('text') or {}).get('indicators')
            },
            conversation_history=history
        )
        
        # Save decision to history (handle dict or plain string)
        if isinstance(decision, dict):
            final_text = decision.get('fullText') or decision.get('full_text') or decision.get('text') or str(decision)
        else:
            final_text = str(decision)
        self.session_manager.add_final_decision(final_text)
        
        # Ask if user wants to continue
        print("\n" + "=" * 70)
        continue_choice = input("\nPress Enter to return to menu...").strip()
        self.run()
    
    def analyze_mood(self, text: str, audio_path: str = None) -> dict:
        """
        Analyze mood from text and optional voice.
        
        Returns:
            {
                'voice': {...} or None,
                'text': {...},
                'aggregated': {...}
            }
        """
        
        results = {}
        
        # Analyze voice if provided
        if audio_path and os.path.exists(audio_path):
            results['voice'] = self.voice_analyzer.analyze(audio_path)
        else:
            results['voice'] = None
        
        # Analyze text (always)
        if text:
            results['text'] = self.sentiment_analyzer.analyze(text)
        else:
            results['text'] = {'moodScore': 5.0, 'sentiment': {}, 'indicators': {}}
        
        # Aggregate
        voice_score = results['voice']['moodScore'] if results['voice'] else results['text']['moodScore']
        voice_conf = results['voice'].get('confidence', 1.0) if results['voice'] else 0.0
        
        results['aggregated'] = self.mood_aggregator.aggregate(
            voice_score=voice_score,
            text_score=results['text']['moodScore'],
            voice_confidence=voice_conf
        )
        
        return results
    
    def get_voice_input(self) -> str:
        """
        Get voice input from user.
        
        Options:
        1. Record now (requires microphone)
        2. Provide existing audio file path
        """
        
        print("\nVOICE INPUT OPTIONS:")
        print("1. Record now (needs microphone + sounddevice)")
        print("2. Provide existing audio file path")
        
        choice = input("Select (1 or 2): ").strip()
        
        if choice == '1':
            return self.record_audio()
        elif choice == '2':
            path = input("Enter audio file path: ").strip()
            if os.path.exists(path):
                return path
            else:
                print(f"⚠️ File not found: {path}")
                return None
        else:
            print("Invalid choice")
            return None
    
    def record_audio(self) -> str:
        """Record audio from microphone."""
        
        if not HAS_AUDIO:
            print("⚠️ sounddevice not installed. Install with: pip install sounddevice soundfile")
            return None
        
        try:
            duration = int(input("Recording duration in seconds (default 10): ").strip() or "10")
            
            print(f"\n🔴 RECORDING for {duration} seconds... SPEAK NOW!")
            
            audio = sd.rec(
                int(duration * self.voice_analyzer.sample_rate),
                samplerate=self.voice_analyzer.sample_rate,
                channels=1
            )
            sd.wait()
            
            # Save to temp file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/recording_{timestamp}.wav"
            os.makedirs("data", exist_ok=True)
            
            sf.write(filename, audio, self.voice_analyzer.sample_rate)
            
            print(f"✅ Recording saved: {filename}\n")
            return filename
            
        except Exception as e:
            print(f"⚠️ Recording failed: {e}")
            return None
    
    def view_history(self):
        """View conversation history."""
        
        history = self.session_manager.get_recent_history(10)
        
        if not history:
            print("\n📭 No conversation history yet.\n")
            return self.run()
        
        print("\n" + "=" * 70)
        print(f"CONVERSATION HISTORY (last {len(history)} interactions)")
        print("=" * 70 + "\n")
        
        for i, conv in enumerate(history, 1):
            print(f"{i}. {conv['timestamp'][:19]}")
            print(f"   Mood: {conv['mood']:.1f}/10 ({conv['category']})")
            print(f"   You said: \"{conv['userText'][:80]}...\"")
            
            if conv.get('llmDecision'):
                print(f"   AI recommended: {conv['llmDecision'][:100]}...")
            
            print()
        
        # Show trend
        trend = self.session_manager.get_mood_trend()
        if trend['trend'] != 'insufficient_data':
            print(f"📊 Overall trend: {trend['trend']} (avg mood: {trend['averageMood']}/10)")
        
        print("\n" + "=" * 70)
        input("\nPress Enter to return to menu...")
        self.run()


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    try:
        # Validate configuration
        Config.validate()
        
        # Create and run app
        app = MoodAnalysisApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)