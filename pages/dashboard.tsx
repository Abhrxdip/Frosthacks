import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import dynamic from 'next/dynamic';
import Layout from '@/components/Layout/Layout';
import Card from '@/components/Card/Card';
import MoodChart from '@/components/MoodChart/MoodChart';
import AIInterventionBot from '@/components/AIInterventionBot/AIInterventionBot';
import { useMood } from '@/hooks/useMood';
import { shouldIntervene } from '@/utils/voiceAnalysis';
import styles from './dashboard.module.css';

// Load 3D components only on client side
const MoodGlobe3D = dynamic(() => import('@/components/MoodGlobe3D/MoodGlobe'), {
  ssr: false,
  loading: () => <div style={{ height: '500px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white' }}>Loading 3D visualization...</div>
});

const MoodCalendar = dynamic(() => import('@/components/MoodCalendar/MoodCalendar'), {
  ssr: false,
  loading: () => <div style={{ height: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white' }}>Loading calendar...</div>
});

const Dashboard: React.FC = () => {
  const router = useRouter();
  const { history, trendStatus, loading, error } = useMood();
  const [showBot, setShowBot] = useState(false);

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('authToken');
    if (!token) {
      router.push('/login');
      return;
    }

    // Check if AI intervention should be triggered
    if (history.length > 0 && shouldIntervene(history)) {
      const lastDismissed = localStorage.getItem('aiInterventionDismissed');
      const oneDayAgo = Date.now() - (24 * 60 * 60 * 1000);
      
      // Show bot if never dismissed or dismissed more than 24 hours ago
      if (!lastDismissed || parseInt(lastDismissed) < oneDayAgo) {
        setTimeout(() => setShowBot(true), 2000);
      }
    }
  }, [router, history]);

  const calculateAverage = (): number => {
    if (history.length === 0) return 0;
    const last7Days = history.slice(0, 7);
    const sum = last7Days.reduce((acc, entry) => acc + entry.mood, 0);
    return Math.round((sum / last7Days.length) * 10) / 10;
  };

  const getCurrentMood = (): number | null => {
    return history.length > 0 ? history[0].mood : null;
  };

  const getTrendIndicator = (): string => {
    if (history.length < 2) return '→';
    const current = history[0].mood;
    const previous = history[1].mood;
    if (current > previous) return '↑';
    if (current < previous) return '↓';
    return '→';
  };

  const getMoodEmoji = (mood: number | null): string => {
    if (mood === null) return '😊';
    if (mood >= 8) return '😄';
    if (mood >= 6) return '😊';
    if (mood >= 4) return '😐';
    if (mood >= 2) return '😔';
    return '😢';
  };

  const getMoodLabel = (mood: number | null): string => {
    if (mood === null) return 'No data yet';
    if (mood >= 8) return 'Great';
    if (mood >= 6) return 'Good';
    if (mood >= 4) return 'Okay';
    if (mood >= 2) return 'Low';
    return 'Very Low';
  };

  const currentMood = getCurrentMood();
  const average = calculateAverage();
  const trend = getTrendIndicator();

  return (
    <Layout>
      <div className={styles.container}>
        <div className={styles.header}>
          <h1>🧠 Your Mental Health Dashboard</h1>
          <p className={styles.subtitle}>Track your emotional journey with AI-powered insights</p>
        </div>

        {loading ? (
          <div className={styles.loading}>Loading your mood data...</div>
        ) : error ? (
          <div className={styles.error}>{error}</div>
        ) : (
          <>
            <div className={styles.summaryCards}>
              <Card className={styles.summaryCard}>
                <div className={styles.cardIcon}>{getMoodEmoji(currentMood)}</div>
                <div className={styles.cardLabel}>Current Mood</div>
                <div className={styles.cardValue}>
                  {currentMood !== null ? `${currentMood}/10` : 'N/A'}
                </div>
                <div className={styles.cardSubtext}>{getMoodLabel(currentMood)}</div>
              </Card>

              <Card className={styles.summaryCard}>
                <div className={styles.cardIcon}>📊</div>
                <div className={styles.cardLabel}>7-Day Average</div>
                <div className={styles.cardValue}>
                  {history.length > 0 ? average : 'N/A'}
                </div>
                <div className={styles.cardSubtext}>
                  {history.length > 0 ? `Based on ${Math.min(7, history.length)} entries` : 'Start journaling'}
                </div>
              </Card>

              <Card className={styles.summaryCard}>
                <div className={styles.cardIcon}>{trend}</div>
                <div className={styles.cardLabel}>Trend</div>
                <div className={styles.cardValue}>
                  {trend === '↑' ? 'Improving' : trend === '↓' ? 'Declining' : 'Stable'}
                </div>
                <div className={styles.cardSubtext}>
                  {history.length >= 2 ? 'Compared to last entry' : 'Need more data'}
                </div>
              </Card>
            </div>

            {/* 3D Mood Globe */}
            <Card className={styles.globeCard}>
              <h2>🌐 Immersive Mood Sphere</h2>
              <p className={styles.chartSubtitle}>Real-time 3D visualization of your emotional journey</p>
              <MoodGlobe3D moodHistory={history} />
            </Card>

            {/* Traditional Chart */}
            <Card className={styles.chartCard}>
              <h2>📈 Mood Trends</h2>
              <p className={styles.chartSubtitle}>Your emotional patterns over time</p>
              <MoodChart data={history} />
            </Card>

            {/* Calendar Heatmap */}
            <Card className={styles.calendarCard}>
              <MoodCalendar moodHistory={history} />
            </Card>

            <Card className={styles.historyCard}>
              <h2>Recent Entries</h2>
              {history.length === 0 ? (
                <div className={styles.emptyHistory}>
                  <p>No journal entries yet. Visit the <a href="/journal">Journal</a> page to get started!</p>
                </div>
              ) : (
                <div className={styles.historyList}>
                  {history.slice(0, 10).map((entry) => (
                    <div key={entry.id} className={styles.historyItem}>
                      <div className={styles.historyDate}>
                        {new Date(entry.date).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric',
                        })}
                      </div>
                      <div className={styles.historyMood}>
                        <span className={styles.moodEmoji}>{getMoodEmoji(entry.mood)}</span>
                        <span className={styles.moodScore}>{entry.mood}/10</span>
                      </div>
                      <div className={styles.historySource}>
                        {entry.source === 'text' ? '✍️ Text' : '🎙️ Voice'}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </>
        )}

        {/* AI Intervention Bot */}
        <AIInterventionBot 
          show={showBot} 
          onClose={() => {
            setShowBot(false);
            localStorage.setItem('aiInterventionDismissed', Date.now().toString());
          }}
          avgMood={average}
          trendStatus={trendStatus?.status as 'positive' | 'stable' | 'negative' || 'stable'}
        />
      </div>
    </Layout>
  );
};

export default Dashboard;
