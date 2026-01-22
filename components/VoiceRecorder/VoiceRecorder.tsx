import React, { useState, useRef, useEffect } from 'react';
import { VoiceAnalyzer, VoiceAnalysis } from '../../utils/voiceAnalysis';
import styles from './VoiceRecorder.module.css';

interface VoiceRecorderProps {
  onRecordingComplete: (blob: Blob, analysis?: VoiceAnalysis) => void;
  isSubmitting: boolean;
}

const VoiceRecorder: React.FC<VoiceRecorderProps> = ({ onRecordingComplete, isSubmitting }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [voiceAnalysis, setVoiceAnalysis] = useState<VoiceAnalysis | null>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const voiceAnalyzerRef = useRef<VoiceAnalyzer | null>(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });
      
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      // Start voice analysis
      voiceAnalyzerRef.current = new VoiceAnalyzer();
      await voiceAnalyzerRef.current.startAnalysis(stream);

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setAudioBlob(blob);
        const url = URL.createObjectURL(blob);
        setAudioURL(url);
        
        // Get final voice analysis
        if (voiceAnalyzerRef.current) {
          const analysis = voiceAnalyzerRef.current.getCurrentFeatures();
          setVoiceAnalysis(analysis);
          voiceAnalyzerRef.current.stopAnalysis();
        }
        
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
  };

  const handleSubmit = () => {
    if (audioBlob) {
      onRecordingComplete(audioBlob, voiceAnalysis || undefined);
    }
  };

  const handleReset = () => {
    setAudioURL(null);
    setAudioBlob(null);
    setRecordingTime(0);
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className={styles.container}>
      <div className={styles.recorderCard}>
        {!isRecording && !audioURL && (
          <div className={styles.readyState}>
            <div className={styles.micIcon}>🎙️</div>
            <h3>Ready to record</h3>
            <p className={styles.hint}>Share what's on your mind (20-30 seconds recommended)</p>
            <button onClick={startRecording} className={styles.recordBtn}>
              Start Recording
            </button>
          </div>
        )}

        {isRecording && (
          <div className={styles.recordingState}>
            <div className={styles.pulse}>
              <div className={styles.pulseRing}></div>
              <div className={styles.micIconRecording}>🎙️</div>
            </div>
            <h3>Recording...</h3>
            <div className={styles.timer}>{formatTime(recordingTime)}</div>
            <button onClick={stopRecording} className={styles.stopBtn}>
              Stop Recording
            </button>
          </div>
        )}

        {audioURL && (
          <div className={styles.previewState}>
            <div className={styles.successIcon}>✅</div>
            <h3>Recording complete</h3>
            <p className={styles.duration}>Duration: {formatTime(recordingTime)}</p>
            
            <audio controls src={audioURL} className={styles.audioPlayer} />
            
            <div className={styles.actions}>
              <button onClick={handleReset} className={styles.resetBtn} disabled={isSubmitting}>
                Record Again
              </button>
              <button onClick={handleSubmit} className={styles.submitBtn} disabled={isSubmitting}>
                {isSubmitting ? 'Submitting...' : 'Submit Voice Note'}
              </button>
            </div>
          </div>
        )}
      </div>

      <div className={styles.tips}>
        <p>💡 <strong>Tip:</strong> Find a quiet space where you feel comfortable expressing yourself</p>
      </div>
    </div>
  );
};

export default VoiceRecorder;
