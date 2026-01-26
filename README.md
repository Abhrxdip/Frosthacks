# 🧠 MindSpace - AI-Powered Mental Health Mood Analysis System

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

> An intelligent mental health companion that uses multimodal AI analysis (voice + text) to track emotional wellbeing and provide personalized recommendations.

---

## 🎯 **Project Overview**

MindSpace is a comprehensive mental health tracking application that combines **voice emotion detection**, **text sentiment analysis**, and **AI-powered recommendations** to help users understand and improve their emotional wellbeing. Unlike traditional text-only mood trackers, MindSpace analyzes both what you say and how you say it to provide deeper insights into your mental state.

### **Key Innovation**
- **Multimodal Analysis**: Combines voice prosody features with text sentiment to detect emotional discrepancies
- **AI-Powered Insights**: Uses LLM (Gemini/GPT/Claude) to generate personalized mental health recommendations
- **Privacy-First**: All voice/text processing happens locally, with only anonymized data sent to LLM APIs
- **Scientific Foundation**: Uses research-backed acoustic features (pitch, jitter, shimmer) validated in clinical studies

---

## 🏗️ **System Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │          Next.js Frontend (Port 3000)                     │   │
│  │  - React Components (Dashboard, Journal, Auth)           │   │
│  │  - 3D Visualizations (Three.js)                          │   │
│  │  - Real-time Voice Recording (Meyda.js)                  │   │
│  │  - Chart & Calendar Components (Recharts)               │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────┬──────────────────────────────────────────────┘
                    │ HTTP/REST API
                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND LAYER                               │
│  ┌────────────────────────────────────────────────────────┐     │
│  │      Node.js/Express Server (Port 5000)                │     │
│  │  - JWT Authentication & User Management                │     │
│  │  - Journal Entry CRUD Operations                       │     │
│  │  - Voice Audio File Handling (Multer)                  │     │
│  │  - API Gateway to Python Mood Analysis System          │     │
│  └────────────────────────────────────────────────────────┘     │
└───────────────────┬──────────────────────────────────────────────┘
                    │ HTTP API Calls
                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                   AI ANALYSIS LAYER                              │
│  ┌────────────────────────────────────────────────────────┐     │
│  │      Python Flask API Server (Port 5001)               │     │
│  │                                                         │     │
│  │  ┌──────────────────────────────────────────────────┐  │     │
│  │  │  Voice Analyzer (Librosa + Parselmouth)          │  │     │
│  │  │  - Pitch (F0) Extraction                         │  │     │
│  │  │  - Jitter (Pitch Perturbation)                   │  │     │
│  │  │  - Shimmer (Amplitude Perturbation)              │  │     │
│  │  │  - Speaking Rate & Energy                        │  │     │
│  │  │  - MFCC Features                                 │  │     │
│  │  └──────────────────────────────────────────────────┘  │     │
│  │                                                         │     │
│  │  ┌──────────────────────────────────────────────────┐  │     │
│  │  │  Sentiment Analyzer (VADER + NLP)                │  │     │
│  │  │  - Polarity Scores (pos/neg/neutral)             │  │     │
│  │  │  - Keyword Extraction                            │  │     │
│  │  │  - Emotional Indicators                          │  │     │
│  │  └──────────────────────────────────────────────────┘  │     │
│  │                                                         │     │
│  │  ┌──────────────────────────────────────────────────┐  │     │
│  │  │  Mood Aggregator                                 │  │     │
│  │  │  - Weighted Combination (60% Voice, 40% Text)    │  │     │
│  │  │  - Discrepancy Detection                         │  │     │
│  │  │  - Confidence Scoring                            │  │     │
│  │  └──────────────────────────────────────────────────┘  │     │
│  │                                                         │     │
│  │  ┌──────────────────────────────────────────────────┐  │     │
│  │  │  LLM Integration                                 │  │     │
│  │  │  - Gemini/GPT/Claude Support                     │  │     │
│  │  │  - Context-Aware Question Generation             │  │     │
│  │  │  - Personalized Recommendations                  │  │     │
│  │  │  - Conversation History Management               │  │     │
│  │  └──────────────────────────────────────────────────┘  │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 **Complete Application Flow**

### **1. User Authentication Flow**
```
User Opens App (localhost:3000)
    ↓
[Register/Login Page]
    ↓
User Submits Credentials
    ↓
Frontend → POST /auth/register or /auth/login → Node.js Backend
    ↓
Backend: Validates credentials, hashes password (bcrypt)
    ↓
Backend: Generates JWT token (7-day expiry)
    ↓
Frontend: Stores token in localStorage
    ↓
[Redirect to Dashboard]
```

### **2. Dashboard Loading Flow**
```
Dashboard Component Mounts
    ↓
useAuth Hook: Validates JWT token
    ↓
useMood Hook: Fetches journal history
    ↓
Frontend → GET /journals (with JWT) → Node.js Backend
    ↓
Backend: Authenticates user, retrieves all journal entries
    ↓
Frontend: Renders mood visualization components:
    - MoodChart (Recharts line graph)
    - MoodCalendar (Heatmap)
    - MoodGlobe3D (Three.js 3D globe)
    - AI Intervention Bot (conditional)
```

### **3. Text Journal Entry Flow**
```
User Clicks "New Entry" → Navigate to /journal
    ↓
User Types Text Entry: "I'm feeling stressed about work"
    ↓
User Clicks "Analyze Mood"
    ↓
Frontend → POST /journals → Node.js Backend
    {
        "type": "text",
        "content": "I'm feeling stressed about work",
        "timestamp": "2026-01-27T10:30:00"
    }
    ↓
Backend → POST /analyze/text → Python Flask API
    ↓
Python: SentimentAnalyzer.analyze()
    - Uses VADER (Valence Aware Dictionary)
    - Calculates compound score: -1.0 to +1.0
    - Extracts emotional keywords
    - Converts to mood score (0-10 scale)
    ↓
Python Returns:
    {
        "moodScore": 4.5,
        "sentiment": {
            "compound": -0.4,
            "positive": 0.1,
            "negative": 0.6,
            "neutral": 0.3
        },
        "indicators": {
            "negative_words": ["stressed"],
            "positive_words": [],
            "dominant_emotion": "anxiety"
        }
    }
    ↓
Backend: Saves to journal storage with mood score
    ↓
Backend → Returns journal entry to frontend
    ↓
Frontend: Updates mood chart & displays result
```

### **4. Voice Journal Entry Flow**
```
User Clicks "Record Voice"
    ↓
Frontend: Requests microphone permission
    ↓
User Records 5-10 second audio message
    ↓
Frontend: Converts recording to WAV/WebM format
    ↓
Frontend → POST /journals (multipart/form-data) → Node.js Backend
    {
        "type": "voice",
        "timestamp": "2026-01-27T10:35:00",
        "audio": [binary audio file]
    }
    ↓
Backend: Saves audio file to uploads/ directory
    ↓
Backend → POST /analyze/voice (multipart) → Python Flask API
    ↓
Python: VoiceAnalyzer.analyze()
    ┌─────────────────────────────────────────┐
    │ 1. Load Audio (Librosa)                 │
    │    - Resample to 16kHz                  │
    │    - Normalize amplitude                │
    └─────────────────────────────────────────┘
    ┌─────────────────────────────────────────┐
    │ 2. Extract Acoustic Features            │
    │                                         │
    │  A. Pitch (F0) - Parselmouth:           │
    │     - Mean pitch (Hz)                   │
    │     - Pitch range (variability)         │
    │     - Higher pitch → Arousal/excitement │
    │     - Lower pitch → Sadness/depression  │
    │                                         │
    │  B. Jitter (Pitch Perturbation):        │
    │     - Cycle-to-cycle pitch variation    │
    │     - High jitter → Stress/anxiety      │
    │     - Normal: < 1%                      │
    │                                         │
    │  C. Shimmer (Amplitude Perturbation):   │
    │     - Cycle-to-cycle amplitude change   │
    │     - High shimmer → Voice strain       │
    │     - Normal: < 3%                      │
    │                                         │
    │  D. Speaking Rate:                      │
    │     - Syllables per second              │
    │     - Fast → Anxiety/excitement         │
    │     - Slow → Depression/fatigue         │
    │                                         │
    │  E. Energy (RMS):                       │
    │     - Average voice intensity           │
    │     - Low energy → Depression           │
    │     - High energy → Positive mood       │
    │                                         │
    │  F. MFCC (Mel-frequency cepstral):      │
    │     - Captures voice timbre             │
    │     - Used in emotion classification    │
    └─────────────────────────────────────────┘
    ┌─────────────────────────────────────────┐
    │ 3. Calculate Mood Score                 │
    │    - Weighted combination of features   │
    │    - Normalized to 0-10 scale           │
    │    - Confidence score (0-1)             │
    └─────────────────────────────────────────┘
    ↓
Python Returns:
    {
        "moodScore": 6.2,
        "confidence": 0.78,
        "features": {
            "pitch_mean": 185.5,
            "pitch_std": 42.3,
            "jitter": 0.012,
            "shimmer": 0.045,
            "speaking_rate": 3.2,
            "energy": 0.68
        },
        "interpretation": {
            "arousal": "moderate",
            "stress_level": "low",
            "voice_quality": "good"
        }
    }
    ↓
Backend: Saves to journal with voice metadata
    ↓
Frontend: Displays voice analysis results
```

### **5. Combined (Text + Voice) Analysis Flow**
```
User Records Voice AND Provides Text
    ↓
Backend: Processes both in parallel
    ├─→ POST /analyze/text → Text analysis
    └─→ POST /analyze/voice → Voice analysis
    ↓
Backend: Receives both scores
    - Text mood: 7.0 (says "I'm fine")
    - Voice mood: 4.5 (voice shows stress)
    ↓
Backend → POST /analyze/combined → Python Flask API
    {
        "textScore": 7.0,
        "voiceScore": 4.5,
        "textData": {...},
        "voiceData": {...}
    }
    ↓
Python: MoodAggregator.combine_scores()
    - Weighted average: 60% voice, 40% text
    - Final score: (4.5 * 0.6) + (7.0 * 0.4) = 5.5
    - Discrepancy detection: |7.0 - 4.5| = 2.5 (HIGH)
    - Flag: "Emotional discrepancy detected"
    ↓
Python Returns:
    {
        "finalMoodScore": 5.5,
        "textScore": 7.0,
        "voiceScore": 4.5,
        "discrepancy": {
            "level": "high",
            "difference": 2.5,
            "interpretation": "User may be masking emotions"
        },
        "dominant_modality": "voice",
        "confidence": 0.82
    }
    ↓
Frontend: Displays combined analysis with warning
    - Shows discrepancy alert
    - Suggests professional support if needed
```

### **6. AI Recommendations Flow**
```
User Clicks "Get AI Insights"
    ↓
Frontend → POST /llm/recommendations → Node.js Backend
    {
        "userId": "user123",
        "recentMoods": [5.5, 6.0, 4.5, 5.0],
        "currentEntry": {
            "text": "I'm fine",
            "voiceFeatures": {...},
            "discrepancy": true
        }
    }
    ↓
Backend → POST /llm/generate-advice → Python Flask API
    ↓
Python: DecisionMaker.generate_recommendations()
    ┌─────────────────────────────────────────┐
    │ 1. Load Conversation History            │
    │    - Previous sessions                  │
    │    - Mood trends                        │
    │    - User context                       │
    └─────────────────────────────────────────┘
    ┌─────────────────────────────────────────┐
    │ 2. Prepare LLM Prompt                   │
    │    - System role: Mental health advisor │
    │    - User mood history                  │
    │    - Current mood analysis              │
    │    - Detected discrepancies             │
    └─────────────────────────────────────────┘
    ┌─────────────────────────────────────────┐
    │ 3. Call LLM API                         │
    │    - Gemini/GPT/Claude (configurable)   │
    │    - Temperature: 0.7 (balanced)        │
    │    - Max tokens: 500                    │
    └─────────────────────────────────────────┘
    ┌─────────────────────────────────────────┐
    │ 4. Save to Conversation History         │
    │    - Store recommendations              │
    │    - Update user context                │
    └─────────────────────────────────────────┘
    ↓
Python Returns:
    {
        "recommendations": [
            "I notice a discrepancy between your words and tone...",
            "Consider taking a short break for deep breathing",
            "Would you like to talk about what's stressing you?"
        ],
        "activities": [
            "5-minute meditation",
            "Walk outside",
            "Call a friend"
        ],
        "resources": [
            "Stress management techniques",
            "Mindfulness exercises"
        ],
        "urgency": "moderate"
    }
    ↓
Frontend: Displays AI recommendations in chat interface
    - Shows as conversation bubbles
    - Provides actionable suggestions
    - Links to resources
```

### **7. AI Intervention Trigger Flow**
```
Background: useMood hook monitors mood history
    ↓
Detection Criteria:
    - 3+ consecutive days with mood < 4.0
    - OR sudden drop > 3 points in 2 days
    - OR high discrepancy scores (> 2.5)
    ↓
Frontend: shouldIntervene() returns true
    ↓
Check localStorage:
    - Has bot been dismissed in last 24 hours?
    - No → Show AI Intervention Bot
    - Yes → Wait for next trigger
    ↓
[AI Intervention Bot appears]
    - Animated entrance
    - Empathetic message
    - Offers resources & professional help
    - User can dismiss or engage
```

---

## 🚀 **Quick Start Guide**

### **Prerequisites**
- Node.js 16+ and npm
- Python 3.8+
- Windows/Mac/Linux OS
- Microphone access (for voice recording)

### **Installation**

```bash
# 1. Clone the repository
git clone https://github.com/Abhrxdip/Frosthacks.git
cd fh

# 2. Run automated setup (installs all dependencies)
setup.bat   # Windows
# or
./setup.sh  # Mac/Linux

# 3. Configure API Keys
# Create mood-analysis-system/.env file:
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_api_key_here

# Get free API key: https://makersuite.google.com/app/apikey
```

### **Starting the Application**

```bash
# Start all servers (Frontend + Backend + AI Analysis)
start-servers.bat   # Windows
# or
./start-servers.sh  # Mac/Linux

# Servers will start on:
# - Frontend: http://localhost:3000
# - Node.js Backend: http://localhost:5000
# - Python API: http://localhost:5001
```

### **Manual Start (Individual Services)**

```bash
# Terminal 1: Python AI Analysis API
cd mood-analysis-system
pip install -r requirements.txt
python api_server.py

# Terminal 2: Node.js Backend
cd backend
npm install
node server.js

# Terminal 3: Next.js Frontend
npm install
npm run dev
```

---

## 📦 **Technology Stack**

### **Frontend (Next.js/React)**
- **Framework**: Next.js 14 (React 18)
- **Styling**: CSS Modules + Framer Motion animations
- **3D Graphics**: Three.js + React Three Fiber
- **Charts**: Recharts (line graphs) + React Calendar Heatmap
- **Audio**: Meyda.js (audio feature extraction), Web Audio API
- **State Management**: Custom hooks (useAuth, useMood, useJournal)
- **HTTP Client**: Axios

### **Backend (Node.js)**
- **Framework**: Express.js
- **Authentication**: JWT (jsonwebtoken) + bcrypt
- **File Upload**: Multer
- **CORS**: Enabled for cross-origin requests
- **Storage**: In-memory (development) - ready for MongoDB/PostgreSQL

### **AI Analysis (Python)**
- **API Framework**: Flask + Flask-CORS
- **Voice Analysis**:
  - `librosa` - Audio signal processing
  - `praat-parselmouth` - Pitch analysis (F0, jitter, shimmer)
  - `numpy` - Numerical computations
- **Text Analysis**:
  - `vaderSentiment` - Sentiment analysis
  - `nltk` - Natural Language Processing
- **LLM Integration**:
  - `google-generativeai` - Gemini API
  - `anthropic` - Claude API (optional)
  - `openai` - GPT API (optional)

---

## 🎨 **Key Features**

### **1. Multimodal Emotion Detection**
- **Text Analysis**: VADER sentiment analysis with keyword extraction
- **Voice Analysis**: Acoustic features (pitch, jitter, shimmer, energy, speaking rate)
- **Combined Analysis**: Weighted fusion (60% voice, 40% text) with discrepancy detection

### **2. AI-Powered Insights**
- **Personalized Recommendations**: Context-aware advice using LLM
- **Conversation History**: Maintains session context for better advice
- **Adaptive Questioning**: AI generates relevant follow-up questions

### **3. Beautiful Visualizations**
- **3D Mood Globe**: Interactive Three.js globe showing mood distribution
- **Mood Chart**: Line graph with trend indicators
- **Mood Calendar**: Heatmap showing mood patterns over time

### **4. Intelligent Interventions**
- **Automatic Triggers**: Detects concerning mood patterns
- **AI Bot**: Proactive support with empathetic messaging
- **Resource Suggestions**: Links to mental health resources

### **5. Privacy & Security**
- **Local Processing**: Voice/text analysis on user's machine
- **JWT Authentication**: Secure token-based auth
- **No Data Selling**: User data never shared or sold
- **Encryption-Ready**: Built with end-to-end encryption support

---

## 🔧 **Configuration**

### **Environment Variables**

**mood-analysis-system/.env**
```env
# LLM Provider (gemini, openai, anthropic)
LLM_PROVIDER=gemini

# API Keys (only one needed)
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Analysis Settings
VOICE_WEIGHT=0.6
TEXT_WEIGHT=0.4
DISCREPANCY_THRESHOLD=2.0
```

### **Backend Configuration**

**backend/server.js**
```javascript
// Mood Analysis API URL
const MOOD_API_URL = process.env.MOOD_API_URL || 'http://localhost:5001';

// JWT Secret (change in production!)
const SECRET = 'mindspace-secret-key-2026';
```

---

## 🧪 **Testing**

```bash
# Run Python tests
cd mood-analysis-system
pytest tests/

# Test individual endpoints
curl http://localhost:5001/health
curl -X POST http://localhost:5001/analyze/text -H "Content-Type: application/json" -d '{"text":"I am happy"}'
```

---

## 📊 **Project Structure**

```
fh/
├── frontend/
│   ├── pages/              # Next.js pages
│   │   ├── index.tsx       # Landing page
│   │   ├── login.tsx       # Login page
│   │   ├── register.tsx    # Registration page
│   │   ├── dashboard.tsx   # Main dashboard
│   │   └── journal.tsx     # Journal entry page
│   ├── components/         # React components
│   │   ├── Layout/         # Layout wrapper
│   │   ├── MoodChart/      # Line chart component
│   │   ├── MoodCalendar/   # Calendar heatmap
│   │   ├── MoodGlobe3D/    # 3D globe visualization
│   │   ├── VoiceRecorder/  # Voice recording UI
│   │   ├── AIInterventionBot/  # AI support bot
│   │   └── ResourceBot/    # Resource suggestions
│   ├── hooks/              # Custom React hooks
│   │   ├── useAuth.ts      # Authentication logic
│   │   ├── useMood.ts      # Mood data fetching
│   │   └── useJournal.ts   # Journal operations
│   ├── utils/              # Utility functions
│   │   ├── api.ts          # API client
│   │   ├── voiceAnalysis.ts  # Voice utilities
│   │   └── encryption.ts   # Security helpers
│   └── styles/             # CSS modules
│
├── backend/
│   ├── server.js           # Express API server
│   ├── uploads/            # Voice audio files
│   └── package.json        # Node dependencies
│
└── mood-analysis-system/   # Python AI Analysis
    ├── api_server.py       # Flask API
    ├── main.py             # CLI application
    ├── config.py           # Configuration
    ├── requirements.txt    # Python dependencies
    ├── services/           # Analysis services
    │   ├── voice_analyzer.py      # Voice emotion detection
    │   ├── sentiment_analyzer.py  # Text sentiment analysis
    │   └── aggregator.py          # Score combination
    ├── llm/                # LLM integration
    │   ├── llm_client.py          # LLM interface
    │   ├── question_generator.py  # Question generation
    │   ├── decision_maker.py      # Recommendations
    │   └── providers/             # API providers
    │       ├── gemini_client.py
    │       ├── anthropic_client.py
    │       └── __init__.py
    ├── utils/              # Utilities
    │   └── session_manager.py     # Conversation history
    ├── data/               # Data storage
    │   ├── sessions.json          # Session history
    │   └── session.json           # Current session
    └── tests/              # Unit tests
```

---

## 🎯 **Hackathon Demo Script**

### **Demo Flow (5 Minutes)**

**1. Opening (30 seconds)**
- Open `http://localhost:3000`
- Quick intro: "MindSpace - AI that understands not just what you say, but how you feel"

**2. Registration (30 seconds)**
- Click Register → Enter demo credentials → Auto-login

**3. Dashboard Tour (1 minute)**
- Point out mood chart, calendar, 3D globe
- Show empty state → "Let's add our first entry"

**4. Text Analysis (1 minute)**
- Navigate to Journal
- Type: "I'm excited about this hackathon but feeling a bit nervous"
- Click Analyze → Show instant mood score (6.5/10)
- Highlight: "VADER sentiment analysis - positive + negative words"

**5. Voice Analysis (1.5 minutes)**
- Click voice recorder
- Record 5 seconds: "Today has been really challenging"
- Show voice features: pitch, jitter, energy
- Explain: "AI analyzes voice stress indicators"
- Show mood score from voice

**6. Discrepancy Detection (1 minute)**
- Record: "I'm totally fine" (but with stressed tone)
- Show text score: 7/10, voice score: 4/10
- Highlight: "Discrepancy detected - may be masking emotions"
- Explain: "This is unique to MindSpace"

**7. AI Recommendations (30 seconds)**
- Click "Get AI Insights"
- Show personalized suggestions from Gemini
- Highlight: "Context-aware using conversation history"

**8. Closing (30 seconds)**
- Back to dashboard → Show updated visualizations
- Quick mention: "AI intervention triggers for concerning patterns"
- Thank judges!

---

## 🏆 **Hackathon Highlights**

### **What Makes MindSpace Special**
1. **Only multimodal mental health tracker** combining voice + text
2. **Scientifically validated** acoustic features (clinical research-backed)
3. **Privacy-first** architecture (local processing)
4. **Beautiful UX** with 3D visualizations and smooth animations
5. **Production-ready** with modular, scalable architecture

### **Technical Achievements**
- ✅ Full-stack application (3 integrated servers)
- ✅ Real-time voice processing with advanced DSP
- ✅ LLM integration with multiple providers
- ✅ Responsive design with modern UI/UX
- ✅ Comprehensive error handling and validation
- ✅ Automated setup and deployment scripts

---

## 📚 **API Documentation**

### **Node.js Backend API (Port 5000)**

#### Authentication
```
POST /auth/register
Body: { "email": string, "password": string }
Response: { "token": string, "user": {...} }

POST /auth/login
Body: { "email": string, "password": string }
Response: { "token": string, "user": {...} }
```

#### Journals
```
GET /journals
Headers: Authorization: Bearer <token>
Response: [{ id, userId, type, content, mood, timestamp }]

POST /journals
Headers: Authorization: Bearer <token>
Body: { "type": "text|voice", "content": string, "audioFile": file }
Response: { id, mood, analysis }

DELETE /journals/:id
Headers: Authorization: Bearer <token>
Response: { message: "Deleted" }
```

### **Python AI API (Port 5001)**

#### Health Check
```
GET /health
Response: { "status": "healthy", "provider": "gemini" }
```

#### Text Analysis
```
POST /analyze/text
Body: { "text": string }
Response: { 
  "moodScore": number,
  "sentiment": {...},
  "indicators": {...}
}
```

#### Voice Analysis
```
POST /analyze/voice
Body: multipart/form-data { "audio": file }
Response: {
  "moodScore": number,
  "confidence": number,
  "features": {...}
}
```

#### Combined Analysis
```
POST /analyze/combined
Body: {
  "textScore": number,
  "voiceScore": number,
  "textData": {...},
  "voiceData": {...}
}
Response: {
  "finalMoodScore": number,
  "discrepancy": {...}
}
```

#### LLM Recommendations
```
POST /llm/generate-advice
Body: {
  "userId": string,
  "moodHistory": number[],
  "currentMood": number,
  "context": {...}
}
Response: {
  "recommendations": string[],
  "activities": string[],
  "resources": string[]
}
```

---

## 🐛 **Troubleshooting**

### **Python API won't start**
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies manually
cd mood-analysis-system
pip install -r requirements.txt

# Check for missing API key
cat .env  # Should have GEMINI_API_KEY
```

### **Frontend can't connect to backend**
```bash
# Check if backend is running
curl http://localhost:5000/health

# Check CORS settings in backend/server.js
# Should have: app.use(cors())
```

### **Voice analysis fails**
```bash
# Install system dependencies (Linux)
sudo apt-get install libsndfile1 portaudio19-dev

# Install system dependencies (Mac)
brew install portaudio

# Check audio file format (should be WAV/WebM)
```

---

## 🚀 **Future Enhancements**

- [ ] Real database integration (PostgreSQL/MongoDB)
- [ ] Mobile app (React Native)
- [ ] Therapist dashboard for professional monitoring
- [ ] Group therapy features
- [ ] Wearable device integration (heart rate, sleep data)
- [ ] Multi-language support
- [ ] Progressive Web App (PWA) with offline support
- [ ] Advanced ML models for emotion classification
- [ ] Integration with calendars for context (work deadlines, etc.)
- [ ] Social support features (anonymous peer groups)

---

## 📄 **License**

MIT License - Feel free to use this project for learning and development.

---

## 👥 **Team**

Built with ❤️ for FrostHacks 2026

---

## 🙏 **Acknowledgments**

- **VADER Sentiment**: Hutto & Gilbert (2014)
- **Voice Analysis Research**: Clinical studies on acoustic markers of depression
- **Three.js Community**: For amazing 3D visualizations
- **Google AI**: For Gemini API access
- **Open Source Community**: For incredible libraries

---

## 📞 **Support**

For issues or questions:
- GitHub Issues: [Create an issue](https://github.com/Abhrxdip/Frosthacks/issues)
- Email: support@mindspace.ai (demo)

---

**⭐ If you find this project helpful, please star the repository!**
