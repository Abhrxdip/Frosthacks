# 🧠 MindSpace - Voice-First AI Mood Analyzer

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

> An intelligent voice-first mental health companion that understands emotions through voice tone, transcription, and adaptive LLM analysis. No rigid timelines or forced tracking - just empathetic, personalized support.

---

## 🎯 **Project Overview**

MindSpace is a revolutionary voice-first mood tracking application that uses **multimodal AI analysis** to understand emotional wellbeing. Unlike traditional text-based trackers with rigid rules, MindSpace:

- **Listens to your voice** and analyzes emotional tone (stress, anxiety, fatigue)
- **Transcribes speech automatically** using advanced speech-to-text
- **Uses LLM reasoning** to understand patterns (not hard-coded thresholds)
- **Adapts analysis windows** based on your data (not fixed 6-day rules)
- **Provides empathetic insights** in natural language

### **Key Innovation**
- **Voice-Primary Design**: Voice recordings capture emotions that text can't express
- **LLM-Adaptive Logic**: No fixed timelines - AI decides when to analyze and intervene
- **Emotional Intelligence**: Detects discrepancies between words and tone
- **Conversational Support**: Human-friendly insights, not clinical diagnostics
- **Privacy-First**: Local voice processing, encrypted storage

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

### **2. Voice Recording Flow (Primary Method)**
```
User Opens Journal → Default: Voice Mode
    ↓
User Clicks "Start Recording"
    ↓
Records 5-60 seconds of voice
    ↓
Frontend → POST /journals (multipart/form-data) → Node.js Backend
    ↓
Backend → POST /analyze/voice → Python Flask API
    ↓
Python AI Analysis:
┌──────────────────────────────────────────┐
│ STEP 1: Acoustic Feature Extraction      │
│ - Pitch (F0): Emotional arousal          │
│ - Jitter: Stress indicators              │
│ - Shimmer: Voice strain                  │
│ - Energy: Depression markers             │
│ - Speaking Rate: Cognitive load          │
└──────────────────────────────────────────┘
┌──────────────────────────────────────────┐
│ STEP 2: Speech-to-Text Transcription     │
│ - Converts voice to text                 │
│ - Uses Google Speech Recognition         │
│ - Captures what was actually said        │
└──────────────────────────────────────────┘
┌──────────────────────────────────────────┐
│ STEP 3: LLM Emotional Analysis           │
│ - Analyzes transcription + voice data    │
│ - Detects: anxiety, stress, sadness,     │
│   calm, fatigue, excitement, etc.        │
│ - Generates natural language summary     │
│ - Assigns mood score (LLM-driven)        │
└──────────────────────────────────────────┘
    ↓
Returns to Frontend:
{
  "transcription": "Today was really hard...",
  "emotionalTone": {
    "primary": "sadness",
    "secondary": ["fatigue", "stress"],
    "intensity": 0.75
  },
  "emotionalSummary": "You sound emotionally drained and overwhelmed.",
  "moodScore": 3.5,
  "confidence": 0.85
}
    ↓
Frontend displays rich emotional insights
```

### **3. Adaptive Mood Pattern Analysis (No Fixed Rules)**
```
User views Dashboard
    ↓
Frontend → POST /analyze/adaptive → Python Flask API
    {
      "moodEntries": [all recent journal entries]
    }
    ↓
Python: AdaptiveMoodAnalyzer
┌──────────────────────────────────────────┐
│ LLM Determines Analysis Window           │
│ - NOT fixed 6-day rule                   │
│ - Considers:                             │
│   • Data density (entries per day)       │
│   • Mood volatility                      │
│   • Emotional urgency                    │
│ - Output: "Analyze past 3 days" or      │
│           "Analyze past week"            │
└──────────────────────────────────────────┘
┌──────────────────────────────────────────┐
│ LLM Analyzes Emotional Patterns          │
│ - NO hard-coded thresholds              │
│ - Identifies:                            │
│   • Mood trends (improving/declining)    │
│   • Recurring emotional themes           │
│   • Warning signs (persistent low mood)  │
│   • Discrepancies (words vs. tone)       │
│ - Decides intervention level             │
└──────────────────────────────────────────┘
    ↓
Returns Adaptive Analysis:
{
  "analysisWindow": "past 4 days",
  "trendDirection": "declining",
  "emotionalPattern": "Persistent fatigue with anxiety spikes",
  "needsAttention": true,
  "supportLevel": "moderate",
  "insights": "You've been pushing through exhaustion...",
  "recommendations": [
    "Consider taking a full rest day",
    "Talk to someone you trust",
    "Professional support might help"
  ]
}
    ↓
Frontend shows personalized, empathetic insights
```

### **4. Intelligent Intervention (LLM-Decided)**
```
Background: System monitors patterns
    ↓
LLM evaluates: "Does this person need support?"
    ↓
NOT based on "3 days under 4/10" rule
    ↓
Based on contextual understanding:
  - Emotional tone over time
  - Voice stress indicators
  - Discrepancies in expression
  - User's unique patterns
    ↓
If LLM says "needs attention" →
    AI Bot appears with empathetic message
    Offers resources, not forced check-ins
    Respects user autonomy
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

### **1. Voice-First Design** 🎤
- **Primary Input Method**: Voice recording is default and recommended
- **Speech-to-Text**: Automatic transcription of what you say
- **Emotional Tone Detection**: AI analyzes how you sound (stress, fatigue, anxiety, calm)
- **Acoustic Analysis**: Pitch, jitter, shimmer, energy, speaking rate
- **Rich Insights**: Natural language emotional summaries

### **2. LLM-Adaptive Analysis** 🤖
- **No Fixed Rules**: Replaces hard-coded thresholds with intelligent reasoning
- **Dynamic Time Windows**: Analysis period adapts to your data (not fixed 6-day tracking)
- **Pattern Recognition**: LLM identifies emotional trends and concerning patterns
- **Contextual Understanding**: Considers your unique emotional baseline
- **Empathetic Communication**: Human-friendly insights, not clinical jargon

### **3. Intelligent Interventions** 🆘
- **LLM-Decided Support**: AI determines when you need help (no arbitrary triggers)
- **Adaptive Support Levels**: none → gentle → moderate → urgent
- **Personalized Recommendations**: Based on your specific patterns
- **No Forced Tracking**: Respects autonomy, doesn't pressure daily check-ins
- **Resource Suggestions**: Links to professional help when appropriate

### **4. Discrepancy Detection** 🎭
- **Words vs. Tone Analysis**: Detects when you say "I'm fine" but voice shows distress
- **Emotional Masking**: Identifies when people hide true feelings
- **Combined Scoring**: 60% voice + 40% text for accuracy
- **Privacy-Respecting**: Alerts user gently, doesn't force disclosure

### **5. Beautiful Visualizations** ✨
- **3D Mood Globe**: Interactive Three.js globe showing mood distribution
- **Adaptive Charts**: Visualization adjusts to your data density
- **Mood Calendar**: Heatmap showing emotional patterns
- **No Streak Pressure**: Visualizations don't guilt-trip for missing days

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
