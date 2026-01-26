# =============================================================================
# api_server.py
# Flask API server for mood analysis system
# =============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback
from datetime import datetime
import tempfile

# Import mood analysis components
from services.voice_analyzer import VoiceAnalyzer
from services.sentiment_analyzer import SentimentAnalyzer
from services.aggregator import MoodAggregator
from services.adaptive_analyzer import AdaptiveMoodAnalyzer
from llm.question_generator import QuestionGenerator
from llm.decision_maker import DecisionMaker
from utils.session_manager import SessionManager
from config import Config

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize components
voice_analyzer = VoiceAnalyzer()
sentiment_analyzer = SentimentAnalyzer()
mood_aggregator = MoodAggregator()
adaptive_analyzer = AdaptiveMoodAnalyzer()
question_generator = QuestionGenerator()
decision_maker = DecisionMaker()
session_manager = SessionManager()

print("✅ Mood Analysis API Server initialized (Voice-first, LLM-adaptive)")

# =============================================================================
# Health Check
# =============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Check if API is running."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'provider': Config.LLM_PROVIDER
    })

# =============================================================================
# Text Analysis
# =============================================================================

@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    """
    Analyze sentiment from text.
    
    Request body:
    {
        "text": "I'm feeling really happy today!"
    }
    
    Returns:
    {
        "moodScore": 8.5,
        "sentiment": {...},
        "indicators": {...}
    }
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        result = sentiment_analyzer.analyze(text)
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Text analysis error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# =============================================================================
# Voice Analysis
# =============================================================================

@app.route('/analyze/voice', methods=['POST'])
def analyze_voice():
    """
    Analyze emotion from voice audio.
    
    Request: multipart/form-data with 'audio' file
    
    Returns:
    {
        "moodScore": 6.5,
        "confidence": 0.85,
        "features": {...}
    }
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            audio_file.save(temp_file.name)
            temp_path = temp_file.name
        
        # Analyze voice
        result = voice_analyzer.analyze(temp_path)
        
        # Clean up temp file
        try:
            os.unlink(temp_path)
        except:
            pass
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Voice analysis error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# =============================================================================
# Combined Analysis
# =============================================================================

@app.route('/analyze/combined', methods=['POST'])
def analyze_combined():
    """
    Analyze both text and voice together.
    
    Request: multipart/form-data with:
    - 'text': text content
    - 'audio': audio file (optional)
    
    Returns:
    {
        "text": {...},
        "voice": {...},
        "aggregated": {
            "overallMood": 7.5,
            "category": "positive",
            ...
        }
    }
    """
    try:
        text = request.form.get('text', '')
        
        result = {
            'text': None,
            'voice': None,
            'aggregated': None
        }
        
        # Analyze text
        if text:
            result['text'] = sentiment_analyzer.analyze(text)
        
        # Analyze voice if provided
        if 'audio' in request.files:
            audio_file = request.files['audio']
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
                audio_file.save(temp_file.name)
                temp_path = temp_file.name
            
            result['voice'] = voice_analyzer.analyze(temp_path)
            
            # Clean up
            try:
                os.unlink(temp_path)
            except:
                pass
        
        # Aggregate if both available
        if result['text'] and result['voice']:
            result['aggregated'] = mood_aggregator.aggregate(
                voice_score=result['voice']['moodScore'],
                text_score=result['text']['moodScore'],
                voice_confidence=result['voice'].get('confidence', 1.0)
            )
        elif result['text']:
            # Only text available
            result['aggregated'] = {
                'overallMood': result['text']['moodScore'],
                'category': mood_aggregator._categorize(result['text']['moodScore']),
                'voiceComponent': None,
                'textComponent': result['text']['moodScore'],
                'discrepancy': None
            }
        elif result['voice']:
            # Only voice available
            result['aggregated'] = {
                'overallMood': result['voice']['moodScore'],
                'category': mood_aggregator._categorize(result['voice']['moodScore']),
                'voiceComponent': result['voice']['moodScore'],
                'textComponent': None,
                'discrepancy': None
            }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Combined analysis error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# =============================================================================
# LLM Question Generation
# =============================================================================

@app.route('/llm/questions', methods=['POST'])
def generate_questions():
    """
    Generate conversation questions using LLM.
    
    Request body (optional):
    {
        "context": "previous conversation context"
    }
    
    Returns:
    {
        "questions": "How are you feeling today? ..."
    }
    """
    try:
        data = request.get_json() or {}
        context = data.get('context', '')
        
        questions = question_generator.generate_initial_questions(context)
        
        return jsonify({'questions': questions})
        
    except Exception as e:
        print(f"❌ Question generation error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# =============================================================================
# LLM Recommendations
# =============================================================================

@app.route('/llm/recommendations', methods=['POST'])
def generate_recommendations():
    """
    Generate personalized recommendations using LLM.
    
    Request body:
    {
        "moodData": {...},
        "userResponses": {...},
        "conversationHistory": [...]
    }
    
    Returns:
    {
        "recommendation": "Based on your mood...",
        "activities": [...],
        "resources": [...]
    }
    """
    try:
        data = request.get_json()
        
        mood_data = data.get('moodData', {})
        user_responses = data.get('userResponses', {})
        conversation_history = data.get('conversationHistory', [])
        
        recommendation = decision_maker.generate_recommendation(
            mood_data=mood_data,
            user_responses=user_responses,
            conversation_history=conversation_history
        )
        
        return jsonify({'recommendation': recommendation})
        
    except Exception as e:
        print(f"❌ Recommendation generation error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# =============================================================================
# Session Management
# =============================================================================

@app.route('/session/add', methods=['POST'])
def add_session():
    """
    Add interaction to session history.
    
    Request body:
    {
        "moodData": {...},
        "userText": "...",
        "llmQuestions": "...",
        "userAudioPath": "..."
    }
    """
    try:
        data = request.get_json()
        
        session_manager.add_interaction(
            mood_data=data.get('moodData', {}),
            user_text=data.get('userText', ''),
            llm_questions=data.get('llmQuestions', ''),
            user_audio_path=data.get('userAudioPath')
        )
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"❌ Session add error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/session/history', methods=['GET'])
def get_history():
    """Get recent conversation history."""
    try:
        history = session_manager.get_recent_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/session/trend', methods=['GET'])
def get_trend():
    """Get mood trend analysis."""
    try:
        trend = session_manager.get_mood_trend()
        return jsonify(trend)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================================================
# Adaptive Mood Analysis (LLM-driven, no fixed rules)
# =============================================================================

@app.route('/analyze/adaptive', methods=['POST'])
def adaptive_mood_analysis():
    """
    Analyze mood history using adaptive LLM-based logic.
    No fixed time windows or hard-coded thresholds.
    
    Request body:
    {
        "moodEntries": [
            {
                "timestamp": "2026-01-27T10:00:00Z",
                "moodScore": 6.5,
                "emotionalTone": {...},
                "transcription": "...",
                "content": "..."
            },
            ...
        ]
    }
    
    Returns:
    {
        "analysisWindow": "past 5 days",
        "trendDirection": "stable|improving|declining|volatile",
        "emotionalPattern": "...",
        "needsAttention": true|false,
        "supportLevel": "none|gentle|moderate|urgent",
        "insights": "Human-friendly analysis",
        "recommendations": [...]
    }
    """
    try:
        data = request.get_json()
        mood_entries = data.get('moodEntries', [])
        
        analysis = adaptive_analyzer.analyze_mood_history(mood_entries)
        
        return jsonify(analysis)
        
    except Exception as e:
        print(f"❌ Adaptive analysis error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# =============================================================================
# Start Server
# =============================================================================

if __name__ == '__main__':
    port = int(os.getenv('MOOD_API_PORT', 5001))
    print(f"\n🚀 Mood Analysis API running on http://localhost:{port}")
    print(f"📊 Using LLM Provider: {Config.LLM_PROVIDER}")
    print(f"🎤 Voice-first, LLM-adaptive analysis enabled")
    print("\nAvailable endpoints:")
    print("  POST /analyze/text")
    print("  POST /analyze/voice (Enhanced with speech-to-text & LLM)")
    print("  POST /analyze/combined")
    print("  POST /analyze/adaptive (LLM-driven pattern analysis)")
    print("  POST /llm/questions")
    print("  POST /llm/recommendations")
    print("  POST /session/add")
    print("  GET  /session/history")
    print("  GET  /session/trend")
    print("  GET  /health")
    print("\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
