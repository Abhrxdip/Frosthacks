import { useState, useEffect } from 'react';
import api from '@/utils/api';
import { isDemoMode, demoMoodHistory, demoTrendStatus } from '@/utils/demoData';

export interface MoodEntry {
  date: string;
  mood: number;
  source: 'text' | 'voice';
  id: string;
}

export interface TrendStatus {
  status: 'stable' | 'fluctuating' | 'negative';
  message: string;
}

export const useMood = () => {
  const [history, setHistory] = useState<MoodEntry[]>([]);
  const [trendStatus, setTrendStatus] = useState<TrendStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMoodHistory = async () => {
    setLoading(true);
    setError(null);
    
    // Check for demo mode first
    if (isDemoMode()) {
      setHistory(demoMoodHistory);
      setLoading(false);
      return;
    }
    
    try {
      const response = await api.get('/mood/history');
      setHistory(response.data.history || []);
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to fetch mood history.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const fetchTrendStatus = async () => {
    // Check for demo mode first
    if (isDemoMode()) {
      setTrendStatus(demoTrendStatus as TrendStatus);
      return;
    }
    
    try {
      const response = await api.get('/mood/trend-status');
      setTrendStatus(response.data);
    } catch (err) {
      console.error('Failed to fetch trend status');
    }
  };

  useEffect(() => {
    fetchMoodHistory();
    fetchTrendStatus();
  }, []);

  return { history, trendStatus, loading, error, refetch: fetchMoodHistory };
};
