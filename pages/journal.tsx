import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '@/components/Layout/Layout';
import Card from '@/components/Card/Card';
import Button from '@/components/Button/Button';
import VoiceRecorder from '@/components/VoiceRecorder/VoiceRecorder';
import { useJournal } from '@/hooks/useJournal';
import { analyzeSentiment } from '@/utils/voiceAnalysis';
import styles from './journal.module.css';

type JournalMode = 'voice' | 'text';  // Voice-first ordering

interface VoiceAnalysisResult {
  transcription?: string;
  emotionalSummary?: string;
  emotionalTone?: {
    primary: string;
    secondary?: string[];
    intensity?: number;
  };
  moodScore?: number;
}

const Journal: React.FC = () => {
  const router = useRouter();
  const [mode, setMode] = useState<JournalMode>('voice');  // Default to voice mode
  const [textContent, setTextContent] = useState('');
  const [voiceAnalysis, setVoiceAnalysis] = useState<VoiceAnalysisResult | null>(null);
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
      setVoiceAnalysis(null);
      setTimeout(() => {
        resetSuccess();
      }, 3000);
    }
  }, [success, resetSuccess]);

  // Real-time sentiment analysis as user types (only for text mode)
  useEffect(() => {
    if (mode === 'text' && textContent.length > 20) {
      const mood = analyzeSentiment(textContent);
      setPredictedMood(mood);
    } else {
      setPredictedMood(null);
    }
  }, [textContent, mode]);

  const handleTextSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (textContent.trim()) {
      const mood = analyzeSentiment(textContent);
      await submitTextJournal({ content: textContent, mood });
    }
  };

  const handleVoiceSubmit = async (audioBlob: Blob, analysis?: VoiceAnalysisResult) => {
    // Store the voice analysis to display insights
    if (analysis) {
      setVoiceAnalysis(analysis);
    }
    
    // Use the LLM-generated mood score if available
    const mood = analysis?.moodScore || 5;
    await submitVoiceJournal(audioBlob, mood, analysis);
  };

  return (
    <Layout>
      <div className={styles.container}>
        <div className={styles.header}>
          <h1>🎤 Voice Your Feelings</h1>
          <p className={styles.subtitle}>
            Share how you're feeling through voice - AI understands both your words and tone
          </p>
        </div>

        <div className={styles.modeToggle}>
          <button
            className={`${styles.modeBtn} ${mode === 'voice' ? styles.active : ''}`}
            onClick={() => setMode('voice')}
          >
            🎙️ Voice Recording (Recommended)
          </button>
          <button
            className={`${styles.modeBtn} ${mode === 'text' ? styles.active : ''}`}
            onClick={() => setMode('text')}
          >
            ✍️ Text Entry
          </button>
        </div>

        {success && (
          <div className={styles.successMessage}>
            ✅ Your emotional check-in was saved. {voiceAnalysis?.emotionalSummary && (
              <span><br />📊 {voiceAnalysis.emotionalSummary}</span>
            )}
          </div>
        )}

        {error && (
          <div className={styles.errorMessage}>
            {error}
          </div>
        )}

        {mode === 'voice' ? (
          <>
            <Card>
              <div className={styles.voiceIntro}>
                <h3>Why voice recording works better:</h3>
                <ul>
                  <li>✅ Captures emotional tone your words might not express</li>
                  <li>✅ Detects stress, fatigue, or anxiety from voice patterns</li>
                  <li>✅ Faster and more natural than typing</li>
                  <li>✅ AI transcribes and analyzes automatically</li>
                </ul>
              </div>
            </Card>
            <VoiceRecorder onRecordingComplete={handleVoiceSubmit} isSubmitting={loading} />
            
            {voiceAnalysis && !loading && (
              <Card>
                <div className={styles.voiceInsights}>
                  <h3>🎭 Your Emotional Snapshot</h3>
                  {voiceAnalysis.transcription && (
                    <div className={styles.transcription}>
                      <strong>What you said:</strong>
                      <p>"{voiceAnalysis.transcription}"</p>
                    </div>
                  )}
                  {voiceAnalysis.emotionalTone && (
                    <div className={styles.emotions}>
                      <strong>Emotions detected:</strong>
                      <p>
                        Primary: {voiceAnalysis.emotionalTone.primary}
                        {voiceAnalysis.emotionalTone.secondary && voiceAnalysis.emotionalTone.secondary.length > 0 && (
                          <span>, Also: {voiceAnalysis.emotionalTone.secondary.join(', ')}</span>
                        )}
                      </p>
                    </div>
                  )}
                  {voiceAnalysis.emotionalSummary && (
                    <div className={styles.summary}>
                      <strong>AI Analysis:</strong>
                      <p>{voiceAnalysis.emotionalSummary}</p>
                    </div>
                  )}
                </div>
              </Card>
            )}
          </>
        ) : (
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
                  placeholder="Type what's on your mind... (Tip: Voice recording captures emotions better)"
                  className={styles.textarea}
                  rows={12}
                  required
                />
                <div className={styles.characterCount}>
                  {textContent.length} characters
                  {predictedMood && (
                    <span className={styles.moodPrediction}>
                      🤖 Estimated Mood: {predictedMood}/10
                    </span>
                  )}
                </div>
              </div>

              <div className={styles.privacyNote}>
                🔒 Encrypted & private | 💡 Try voice recording for better emotional insights
              </div>

              <Button type="submit" disabled={loading || !textContent.trim()} fullWidth>
                {loading ? 'Analyzing...' : 'Save Entry'}
              </Button>
            </form>
          </Card>
        )}

        <div className={styles.supportText}>
          <p>💙 This is a judgment-free space. Your feelings matter, and expressing them is healthy.</p>
          <p>🎯 Voice recordings provide richer emotional insights than text alone.</p>
        </div>
      </div>
    </Layout>
  );
};

export default Journal;
