import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '@/components/Layout/Layout';
import Card from '@/components/Card/Card';
import Button from '@/components/Button/Button';
import VoiceRecorder from '@/components/VoiceRecorder/VoiceRecorder';
import { useJournal } from '@/hooks/useJournal';
import { analyzeSentiment } from '@/utils/voiceAnalysis';
import styles from './journal.module.css';

type JournalMode = 'text' | 'voice';

const Journal: React.FC = () => {
  const router = useRouter();
  const [mode, setMode] = useState<JournalMode>('text');
  const [textContent, setTextContent] = useState('');
  const [predictedMood, setPredictedMood] = useState<number | null>(null);
  const { submitTextJournal, submitVoiceJournal, loading, error, success, resetSuccess } = useJournal();

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('authToken');
    if (!token) {
      router.push('/login');
    }
  }, [router]);

  useEffect(() => {
    if (success) {
      // Reset form on success
      setTextContent('');
      setPredictedMood(null);
      setTimeout(() => {
        resetSuccess();
      }, 3000);
    }
  }, [success, resetSuccess]);

  // Real-time sentiment analysis as user types
  useEffect(() => {
    if (textContent.length > 20) {
      const mood = analyzeSentiment(textContent);
      setPredictedMood(mood);
    } else {
      setPredictedMood(null);
    }
  }, [textContent]);

  const handleTextSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (textContent.trim()) {
      const mood = analyzeSentiment(textContent);
      await submitTextJournal({ content: textContent, mood });
    }
  };

  const handleVoiceSubmit = async (audioBlob: Blob, voiceAnalysis?: any) => {
    // Use voice analysis mood if available
    const mood = voiceAnalysis?.moodScore || 5;
    await submitVoiceJournal(audioBlob, mood);
  };

  return (
    <Layout>
      <div className={styles.container}>
        <div className={styles.header}>
          <h1>Your Journal</h1>
          <p className={styles.subtitle}>Express yourself freely in your private space</p>
        </div>

        <div className={styles.modeToggle}>
          <button
            className={`${styles.modeBtn} ${mode === 'text' ? styles.active : ''}`}
            onClick={() => setMode('text')}
          >
            ✍️ Text Journal
          </button>
          <button
            className={`${styles.modeBtn} ${mode === 'voice' ? styles.active : ''}`}
            onClick={() => setMode('voice')}
          >
            🎙️ Voice Note
          </button>
        </div>

        {success && (
          <div className={styles.successMessage}>
            ✅ Journal entry saved successfully! Your thoughts are safe and private.
          </div>
        )}

        {error && (
          <div className={styles.errorMessage}>
            {error}
          </div>
        )}

        {mode === 'text' ? (
          <Card>
            <form onSubmit={handleTextSubmit} className={styles.textForm}>
              <div className={styles.formGroup}>
                <label htmlFor="journal" className={styles.label}>
                  What's on your mind today?
                </label>
                <textarea
                  id="journal"
                  value={textContent}
                  onChange={(e) => setTextContent(e.target.value)}
                  placeholder="Write freely... No one is judging. This space is just for you."
                  className={styles.textarea}
                  rows={12}
                  required
                />
                <div className={styles.characterCount}>
                  {textContent.length} characters
                  {predictedMood && (
                    <span className={styles.moodPrediction}>
                      🤖 AI Mood Score: {predictedMood}/10
                    </span>
                  )}
                </div>
              </div>

              <div className={styles.privacyNote}>
                🔒 Your entry will be encrypted before being saved | 🤖 AI analyzes sentiment automatically
              </div>

              <Button type="submit" disabled={loading || !textContent.trim()} fullWidth>
                {loading ? 'Saving...' : 'Save Journal Entry'}
              </Button>
            </form>
          </Card>
        ) : (
          <VoiceRecorder onRecordingComplete={handleVoiceSubmit} isSubmitting={loading} />
        )}

        <div className={styles.supportText}>
          <p>Remember: This is a judgment-free space. Your feelings are valid, and expressing them is a sign of strength.</p>
        </div>
      </div>
    </Layout>
  );
};

export default Journal;
