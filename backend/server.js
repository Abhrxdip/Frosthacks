const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const multer = require('multer');
const path = require('path');

const app = express();
const upload = multer({ dest: 'uploads/' });

// Middleware
app.use(cors());
app.use(express.json());

// In-memory storage (replace with database in production)
const users = [];
const journals = [];
const SECRET = 'mindspace-secret-key-2026';

// Auth middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ message: 'No token provided' });
  }

  jwt.verify(token, SECRET, (err, user) => {
    if (err) {
      return res.status(401).json({ message: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};

// ==================== AUTH ENDPOINTS ====================

// Register
app.post('/auth/register', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Check if user exists
    if (users.find(u => u.email === email)) {
      return res.status(400).json({ message: 'Email already exists' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // Create user
    const user = {
      id: Date.now().toString(),
      email,
      password: hashedPassword,
      createdAt: new Date()
    };
    
    users.push(user);

    // Generate token
    const token = jwt.sign({ userId: user.id, email: user.email }, SECRET, { expiresIn: '7d' });

    console.log(`✅ User registered: ${email}`);
    res.status(201).json({
      token,
      user: { id: user.id, email: user.email }
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ message: 'Registration failed' });
  }
});

// Login
app.post('/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Find user
    const user = users.find(u => u.email === email);
    if (!user) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Check password
    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Generate token
    const token = jwt.sign({ userId: user.id, email: user.email }, SECRET, { expiresIn: '7d' });

    console.log(`✅ User logged in: ${email}`);
    res.json({
      token,
      user: { id: user.id, email: user.email }
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ message: 'Login failed' });
  }
});

// ==================== JOURNAL ENDPOINTS ====================

// Simple sentiment analysis function
function analyzeSentiment(text) {
  const positiveWords = ['happy', 'joy', 'love', 'excellent', 'good', 'great', 'wonderful', 
    'fantastic', 'amazing', 'positive', 'excited', 'grateful', 'blessed', 'peaceful', 
    'calm', 'better', 'improved', 'progress', 'success'];
  
  const negativeWords = ['sad', 'angry', 'hate', 'bad', 'terrible', 'awful', 'horrible',
    'depressed', 'anxious', 'worried', 'scared', 'lonely', 'hopeless', 'stressed', 
    'overwhelmed', 'exhausted', 'tired', 'hurt', 'pain'];

  const words = text.toLowerCase().split(/\s+/);
  let score = 5; // Neutral baseline

  words.forEach(word => {
    if (positiveWords.includes(word)) score += 0.5;
    if (negativeWords.includes(word)) score -= 0.5;
  });

  // Detect negation
  const negationPattern = /(not|no|never|don't|doesn't|didn't|won't|wouldn't|can't|couldn't)\s+(\w+)/gi;
  const matches = text.toLowerCase().match(negationPattern);
  if (matches) score -= matches.length * 0.3;

  // Detect exclamation (enthusiasm)
  const exclamations = (text.match(/!/g) || []).length;
  score += exclamations * 0.2;

  return Math.max(1, Math.min(10, Math.round(score)));
}

// Submit text journal
app.post('/journal/text', authenticateToken, (req, res) => {
  try {
    let { content, mood } = req.body;
    
    // If no mood provided, use sentiment analysis
    if (!mood && content) {
      mood = analyzeSentiment(content);
      console.log(`🤖 AI analyzed mood: ${mood}/10`);
    }
    
    const journal = {
      id: Date.now().toString(),
      userId: req.user.userId,
      content,
      mood: mood || 5,
      source: 'text',
      date: new Date().toISOString(),
      createdAt: new Date()
    };
    
    journals.push(journal);
    
    console.log(`📝 Text journal created by user ${req.user.email}`);
    res.status(201).json({
      id: journal.id,
      mood: journal.mood,
      source: 'text',
      createdAt: journal.date
    });
  } catch (error) {
    console.error('Text journal error:', error);
    res.status(500).json({ message: 'Failed to save journal' });
  }
});

// Submit voice journal
app.post('/journal/voice', authenticateToken, upload.single('audio'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ message: 'No audio file provided' });
    }

    const mood = req.body.mood ? parseInt(req.body.mood) : 5;

    const journal = {
      id: Date.now().toString(),
      userId: req.user.userId,
      audioPath: req.file.path,
      mood: mood,
      source: 'voice',
      date: new Date().toISOString(),
      createdAt: new Date()
    };
    
    journals.push(journal);
    
    console.log(`🎙️ Voice journal created by user ${req.user.email} (mood: ${mood})`);
    res.status(201).json({
      id: journal.id,
      mood: journal.mood,
      source: 'voice',
      audioUrl: `/uploads/${req.file.filename}`,
      createdAt: journal.date
    });
  } catch (error) {
    console.error('Voice journal error:', error);
    res.status(500).json({ message: 'Failed to save voice note' });
  }
});

// ==================== MOOD ENDPOINTS ====================

// Get mood history
app.get('/mood/history', authenticateToken, (req, res) => {
  try {
    const userJournals = journals
      .filter(j => j.userId === req.user.userId)
      .sort((a, b) => new Date(b.date) - new Date(a.date))
      .slice(0, 30); // Last 30 entries

    const history = userJournals.map(j => ({
      id: j.id,
      date: j.date,
      mood: j.mood,
      source: j.source
    }));

    console.log(`📊 Mood history retrieved for ${req.user.email}: ${history.length} entries`);
    res.json({ history });
  } catch (error) {
    console.error('Mood history error:', error);
    res.status(500).json({ message: 'Failed to fetch mood history' });
  }
});

// Get trend status
app.get('/mood/trend-status', authenticateToken, (req, res) => {
  try {
    const userJournals = journals
      .filter(j => j.userId === req.user.userId)
      .sort((a, b) => new Date(b.date) - new Date(a.date))
      .slice(0, 7); // Last 7 entries

    if (userJournals.length === 0) {
      return res.json({
        status: 'stable',
        message: 'Start journaling to track your mood trends'
      });
    }

    // Calculate average mood
    const avgMood = userJournals.reduce((sum, j) => sum + j.mood, 0) / userJournals.length;

    let status, message;
    if (avgMood >= 7) {
      status = 'stable';
      message = 'Your mood has been stable and positive';
    } else if (avgMood >= 4) {
      status = 'fluctuating';
      message = 'Your mood has been fluctuating recently';
    } else {
      status = 'negative';
      message = 'Your mood has been low recently';
    }

    console.log(`📈 Trend status for ${req.user.email}: ${status} (avg: ${avgMood.toFixed(1)})`);
    res.json({ status, message, avgMood: parseFloat(avgMood.toFixed(1)) });
  } catch (error) {
    console.error('Trend status error:', error);
    res.status(500).json({ message: 'Failed to fetch trend status' });
  }
});

// ==================== START SERVER ====================

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`\n🚀 MindSpace Backend Server Running!`);
  console.log(`📍 URL: http://localhost:${PORT}`);
  console.log(`\n📋 Available endpoints:`);
  console.log(`   POST /auth/register    - Create account`);
  console.log(`   POST /auth/login       - Login`);
  console.log(`   POST /journal/text     - Submit text journal`);
  console.log(`   POST /journal/voice    - Submit voice note`);
  console.log(`   GET  /mood/history     - Get mood history`);
  console.log(`   GET  /mood/trend-status - Get trend status`);
  console.log(`\n💡 Connect frontend: http://localhost:3000\n`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('👋 Server shutting down...');
  process.exit(0);
});
