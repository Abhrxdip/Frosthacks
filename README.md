# 🌟 MindSpace - AI-Powered Mental Health Mood Tracker

A cutting-edge, secure mental health journaling application with 3D visualizations, voice analysis, and proactive AI intervention. Built for hackathons and real-world impact.

**🏆 Hackathon-Ready Features:**
- 3D mood visualization with Three.js
- Real-time sentiment analysis (NLP)
- Voice clarity analysis (pitch, tone, energy)
- Proactive AI chatbot intervention
- Interactive mood heatmap calendar

---

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
npm install
cd backend && npm install
```

### 2. Configure Environment
Create a `.env.local` file:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
NEXT_PUBLIC_ENCRYPTION_KEY=Mh7$k2Pq9#xLz4!nR8wE5@vB3jY6*cF1
```

### 3. Run Both Servers
**Terminal 1 - Backend:**
```bash
cd backend
node server.js
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

Open [http://localhost:3000](http://://localhost:3000) in your browser.

---

## 🎯 Hackathon Problem Statement

**Challenge:** Students face intense academic pressure but rarely seek help due to stigma. Current systems are reactive, not proactive.

**Our Solution:** AI-powered mood tracking using:
1. **Voice Clarity Analysis** - Analyzes jitter, shimmer, pitch, tone
2. **Sentiment Analysis** - NLP on text entries (VADER-like approach)
3. **Trend Detection** - Identifies consistent negative patterns
4. **Proactive Intervention** - AI chatbot initiates conversation when needed

---

## 📋 Core Features

### 🤖 AI & Machine Learning

**Real-Time Sentiment Analysis**
- Analyzes text as you type
- Predicts mood score (1-10)
- Considers positive/negative words, negation, exclamations
- Auto-applies mood score on submission

**Voice Analysis Engine**
- Analyzes voice clarity using Meyda library
- Extracts: pitch, energy, RMS, zero-crossing rate
- Calculates mood from voice features
- Privacy-first: analyzes audio patterns, not content

**Proactive AI Intervention**
- Monitors mood trends automatically
- Triggers when 7-day average < 4 OR consistent decline detected
- Conversational AI chatbot
- Suggests campus resources, breathing exercises
- 24-hour cooldown to avoid spam

### 🌐 3D Visualizations

**Interactive Mood Globe (Three.js)**
- Rotating 3D sphere showing mood data
- Color changes based on average mood (red → yellow → green)
- Particles represent individual entries
- OrbitControls for interaction
- Mesmerizing distortion effects

**Mood Calendar Heatmap**
- 6-month history at a glance
- GitHub-style contribution graph
- Color intensity = mood level
- Hover tooltips with details

### 🔐 Security & Privacy

**Client-Side Encryption**
- AES encryption before data leaves browser
- Backend stores only encrypted data
- Configurable encryption key

**Voice Recording**
- Microphone access with permission
- Real-time recording timer
- Audio playback preview
- Secure upload to backend

**📊 Mood Visualization**
- Interactive mood charts over time
- 7-day average calculations
- Color-coded mood zones (Green/Yellow/Red)
- Historical entry browser

**🤖 Proactive Support Bot**
- Appears when mood trends negative
- Suggests campus resources
- Gentle, non-intrusive messaging
- 24-hour reminder cooldown

---

## 🏗️ How It Works

### Architecture

```
Frontend (Next.js)
    ↓
Custom Hooks (useAuth, useJournal, useMood)
    ↓
API Layer (Axios)
    ↓
Backend API (Your Server)
    ↓
Database
```

### Key Technologies

| Technology | Purpose |
|------------|---------|
| **Next.js 14** | React framework for pages and routing |
| **TypeScript** | Type-safe code |
| **Recharts** | Interactive mood charts |
| **crypto-js** | Client-side encryption |
| **Axios** | API communication |
| **CSS Modules** | Component-scoped styling |

### Data Flow

1. **User Action** (e.g., submit journal)
2. **Encryption** (text content encrypted client-side)
3. **API Request** (sent to backend with JWT token)
4. **Backend Processing** (store, analyze mood)
5. **Response** (success/error)
6. **UI Update** (show feedback to user)

---

## 📂 Project Structure

```
fh/
├── pages/                    # Next.js pages (routes)
│   ├── index.tsx            # Home (auto-redirect)
│   ├── login.tsx            # Login page
│   ├── register.tsx         # Registration
│   ├── dashboard.tsx        # Mood dashboard
│   └── journal.tsx          # Journaling page
│
├── components/              # Reusable UI components
│   ├── Layout/              # Navigation wrapper
│   ├── Button/              # Button component
│   ├── Card/                # Card container
│   ├── MoodChart/           # Chart visualization
│   ├── VoiceRecorder/       # Audio recording
│   └── ResourceBot/         # Support popup
│
├── hooks/                   # Custom React hooks
│   ├── useAuth.ts           # Login/register logic
│   ├── useJournal.ts        # Journal submissions
│   └── useMood.ts           # Mood data fetching
│
├── utils/                   # Utility functions
│   ├── api.ts               # Axios configuration
│   └── encryption.ts        # AES encryption
│
└── styles/
    └── globals.css          # Global styles & CSS variables
```

---

## 🔌 Backend API Requirements

Your backend must provide these endpoints:

### Authentication
```
POST /auth/register
Body: { "email": "user@example.com", "password": "password123" }
Returns: { "token": "jwt-token" }

POST /auth/login
Body: { "email": "user@example.com", "password": "password123" }
Returns: { "token": "jwt-token" }
```

### Journal Submissions
```
POST /journal/text
Headers: Authorization: Bearer {token}
Body: { "content": "encrypted-text", "mood": 7 }

POST /journal/voice
Headers: Authorization: Bearer {token}
Body: FormData with 'audio' file (WebM format)
```

### Mood Data
```
GET /mood/history
Headers: Authorization: Bearer {token}
Returns: { "history": [{ "id": "1", "date": "2026-01-22", "mood": 7, "source": "text" }] }

GET /mood/trend-status
Headers: Authorization: Bearer {token}
Returns: { "status": "negative", "message": "..." }
```

**Note:** All authenticated endpoints require `Authorization: Bearer {token}` header.

---

## 🎨 Key Features Explained

### 1. Voice Recording
- Uses browser's **MediaRecorder API**
- Steps:
  1. Click "Start Recording"
  2. Browser asks for microphone permission
  3. Records audio (WebM format)
  4. Shows live timer
  5. Click "Stop" to preview
  6. Submit to backend

### 2. Mood Chart
- Built with **Recharts** library
- Shows mood (1-10 scale) over time
- Color zones:
  - **Green (7-10)**: Stable mood
  - **Yellow (4-6)**: Fluctuating
  - **Red (1-3)**: Low mood
- Hover for details

### 3. Encryption
- Journal text encrypted **before** sending to server
- Uses AES encryption (crypto-js)
- Encryption key from `.env.local`
- Decryption happens server-side (if needed)

### 4. Resource Bot
- Triggered when backend returns `"status": "negative"`
- Appears bottom-right after 2 seconds
- Options:
  - Show campus resources
  - Remind me later (24hr cooldown)
  - I'm okay for now
- Fully dismissible

---

## 🎯 User Flow

### First Time User
1. Visit app → Redirected to `/login`
2. Click "Create one" → Go to `/register`
3. Fill email, password, confirm password
4. Submit → Account created, JWT token saved
5. Auto-redirect to `/dashboard`

### Existing User
1. Visit app → Redirected to `/login`
2. Enter credentials
3. Click "Sign In" → JWT token saved
4. Redirect to `/dashboard`

### Creating a Journal Entry
1. Click "Journal" in navigation
2. Choose "Text Journal" or "Voice Note"
3. **Text**: Write entry, click "Save"
4. **Voice**: Record, preview, submit
5. Success message appears
6. Entry saved to backend

### Viewing Mood Trends
1. Navigate to `/dashboard`
2. See summary cards:
   - Current mood
   - 7-day average
   - Trend indicator (↑ ↓ →)
3. View chart showing mood over time
4. Browse recent entries below

---

## 🔧 Configuration

### Environment Variables (`.env.local`)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Your backend API URL | `http://localhost:5000` |
| `NEXT_PUBLIC_ENCRYPTION_KEY` | Encryption secret (32+ chars) | `my-secure-key-123` |

### Customizing Colors

Edit `styles/globals.css`:
```css
:root {
  --color-primary: #9C89E3;    /* Main purple */
  --color-secondary: #7EC8E3;  /* Accent blue */
  --color-success: #A8D8B9;    /* Success green */
  /* etc. */
}
```

### Changing Backend URL

Update `.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=https://your-api.com
```

---

## 🐛 Common Issues

### "Port 3000 already in use"
```bash
# Use different port
npm run dev -- -p 3001
```

### "Cannot access microphone"
- Check browser permissions (Settings → Privacy → Microphone)
- Use HTTPS in production
- Try Chrome or Firefox

### "API connection failed"
- Verify backend is running
- Check `.env.local` has correct URL
- Look for CORS errors in browser console

### TypeScript errors
```bash
# Rebuild the project
npm run build
```

---

## 📦 Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

The app will be optimized and ready for deployment.

---

## 🌐 Browser Support

| Browser | Version | Voice Recording |
|---------|---------|-----------------|
| Chrome | 60+ | ✅ |
| Firefox | 55+ | ✅ |
| Safari | 11+ | ✅ (HTTPS required) |
| Edge | 79+ | ✅ |

---

## 🔒 Security

- **Encryption**: Journal text encrypted client-side before sending
- **JWT Tokens**: Secure authentication
- **Auto-logout**: On 401 errors
- **HTTPS**: Recommended for production
- **No logging**: Sensitive data never logged

---

## 💜 Design Philosophy

This app is built with **mental health in mind**:

✅ **Non-clinical language** - No medical jargon  
✅ **Calming colors** - Soft purples and blues  
✅ **Gentle tone** - Supportive, never alarming  
✅ **User control** - Everything is dismissible  
✅ **Privacy first** - Encryption + clear notices  

---

## 📞 Support Resources

If you need help:
- **Crisis Hotline**: 988 (US)
- **Crisis Text**: HOME to 741741
- **Campus Resources**: Contact your student wellness center

---

## 📝 Summary

**MindSpace** is a complete mental health journaling app that:
- Lets students journal via text or voice
- Tracks mood trends with beautiful charts
- Proactively suggests support when needed
- Keeps everything private with encryption
- Works on mobile, tablet, and desktop

**Tech:** Next.js, TypeScript, React, Recharts  
**Time to setup:** 5 minutes  
**Lines of code:** ~3,000  

---

**Built with 💜 for student mental wellness**
