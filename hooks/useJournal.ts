import { useState } from 'react';
import api from '@/utils/api';
import { encryptData } from '@/utils/encryption';
import { isDemoMode } from '@/utils/demoData';

interface TextJournalData {
  content: string;
  mood?: number;
}

export const useJournal = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const submitTextJournal = async (data: TextJournalData) => {
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Demo mode simulation
      if (isDemoMode()) {
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate network delay
        setSuccess(true);
        return { success: true };
      }

      const encryptedContent = encryptData(data.content);
      await api.post('/journal/text', {
        content: encryptedContent,
        mood: data.mood,
      });
      setSuccess(true);
      return { success: true };
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to submit journal. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const submitVoiceJournal = async (audioBlob: Blob, mood?: number) => {
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Demo mode simulation
      if (isDemoMode()) {
        await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate network delay
        setSuccess(true);
        return { success: true };
      }

      const formData = new FormData();
      formData.append('audio', audioBlob, 'voice-note.webm');
      if (mood) {
        formData.append('mood', mood.toString());
      }

      await api.post('/journal/voice', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSuccess(true);
      return { success: true };
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to submit voice note. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const resetSuccess = () => setSuccess(false);

  return { submitTextJournal, submitVoiceJournal, loading, error, success, resetSuccess };
};
