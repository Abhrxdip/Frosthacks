import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styles from './AIInterventionBot.module.css';

interface Message {
  id: string;
  text: string;
  sender: 'bot' | 'user';
  timestamp: Date;
}

interface AIInterventionBotProps {
  show: boolean;
  onClose: () => void;
  avgMood: number;
  trendStatus: 'positive' | 'stable' | 'negative';
}

const AIInterventionBot: React.FC<AIInterventionBotProps> = ({ 
  show, 
  onClose, 
  avgMood,
  trendStatus 
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState('');
  const [stage, setStage] = useState<'greeting' | 'listening' | 'resources'>('greeting');

  useEffect(() => {
    if (show && messages.length === 0) {
      // Initial greeting based on mood trend
      setTimeout(() => {
        addBotMessage(getInitialGreeting());
      }, 500);
    }
  }, [show]);

  const getInitialGreeting = (): string => {
    if (trendStatus === 'negative') {
      return "Hi there 👋 I noticed your mood has been lower recently. I'm here to listen and help. How are you feeling today?";
    } else if (avgMood < 4) {
      return "Hey 👋 I wanted to check in with you. It seems like things might be tough right now. Would you like to talk about it?";
    }
    return "Hello! 👋 I'm your wellness companion. I noticed some patterns in your mood tracking. Want to chat about how you're doing?";
  };

  const addBotMessage = (text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'bot',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const addUserMessage = (text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const handleSend = () => {
    if (!userInput.trim()) return;

    addUserMessage(userInput);
    const input = userInput.toLowerCase();
    setUserInput('');

    // Simple response logic
    setTimeout(() => {
      if (stage === 'greeting') {
        if (input.includes('not good') || input.includes('bad') || input.includes('sad')) {
          addBotMessage("I hear you, and I'm sorry you're going through this. Remember, it's okay to not be okay. Can you tell me what's been weighing on you?");
          setStage('listening');
        } else if (input.includes('okay') || input.includes('fine')) {
          addBotMessage("That's good to hear! Sometimes 'okay' is a great place to start. Would you like some resources to help maintain or improve your wellbeing?");
          setStage('resources');
        } else {
          addBotMessage("Thank you for sharing. Your feelings are valid. Would you like me to suggest some resources that might help?");
          setStage('listening');
        }
      } else if (stage === 'listening') {
        if (input.includes('yes') || input.includes('sure') || input.includes('help')) {
          showResources();
        } else {
          addBotMessage("I understand. Just know that I'm here whenever you need support. Would you like to see some wellness resources?");
          setStage('resources');
        }
      } else {
        addBotMessage("Feel free to come back anytime. Take care of yourself! 💚");
      }
    }, 1000);
  };

  const showResources = () => {
    setStage('resources');
    addBotMessage("Here are some resources that might help:");
    
    setTimeout(() => {
      addBotMessage(`
🏥 **Campus Counseling Services**
• Available 24/7
• Free confidential sessions
• Call: 1-800-WELLNESS

🧘‍♀️ **Mindfulness & Meditation**
• Guided breathing exercises
• Stress reduction techniques
• Available in the app

📞 **Crisis Hotline**
• National Suicide Prevention: 988
• Crisis Text Line: Text HOME to 741741
• SAMHSA Helpline: 1-800-662-4357

💬 **Peer Support Groups**
• Join anonymous group sessions
• Connect with others who understand
• Every Monday & Thursday 6PM

Would you like me to connect you with any of these?
      `);
    }, 1500);
  };

  const handleQuickAction = (action: string) => {
    if (action === 'breathing') {
      addBotMessage("Great choice! Let's do a quick breathing exercise together. Close your eyes and take a deep breath in for 4 counts... Hold for 4... Exhale for 4... Repeat 3 times. 🌬️");
    } else if (action === 'counseling') {
      addBotMessage("I'll connect you to campus counseling services. They offer free, confidential sessions. Would you like their contact information?");
    } else if (action === 'later') {
      addBotMessage("That's okay! I'll be here whenever you're ready. Take care! 💚");
      setTimeout(() => onClose(), 2000);
    }
  };

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          className={styles.overlay}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className={styles.chatContainer}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
          >
            {/* Header */}
            <div className={styles.header}>
              <div className={styles.headerTitle}>
                <div className={styles.botAvatar}>🤖</div>
                <div>
                  <h3>Wellness Companion</h3>
                  <span className={styles.status}>Here to help</span>
                </div>
              </div>
              <button className={styles.closeBtn} onClick={onClose}>✕</button>
            </div>

            {/* Messages */}
            <div className={styles.messages}>
              {messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  className={`${styles.message} ${styles[msg.sender]}`}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <div className={styles.messageContent}>
                    {msg.text}
                  </div>
                  <div className={styles.timestamp}>
                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Quick Actions */}
            {stage === 'greeting' && messages.length > 0 && (
              <div className={styles.quickActions}>
                <button onClick={() => handleQuickAction('breathing')}>
                  🌬️ Breathing Exercise
                </button>
                <button onClick={() => handleQuickAction('counseling')}>
                  💬 Talk to Counselor
                </button>
                <button onClick={() => handleQuickAction('later')}>
                  ⏰ Maybe Later
                </button>
              </div>
            )}

            {/* Input */}
            <div className={styles.inputArea}>
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type your message..."
                className={styles.input}
              />
              <button onClick={handleSend} className={styles.sendBtn}>
                Send
              </button>
            </div>

            {/* Disclaimer */}
            <div className={styles.disclaimer}>
              💚 This is not professional medical advice. For emergencies, call 911.
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default AIInterventionBot;
