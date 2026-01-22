import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { MoodEntry } from '@/hooks/useMood';
import styles from './MoodChart.module.css';

interface MoodChartProps {
  data: MoodEntry[];
}

const MoodChart: React.FC<MoodChartProps> = ({ data }) => {
  // Transform data for the chart
  const chartData = data.map(entry => ({
    date: new Date(entry.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    mood: entry.mood,
    fullDate: entry.date,
  })).reverse(); // Show oldest to newest

  const getColorZone = (mood: number): string => {
    if (mood >= 7) return 'var(--color-success)';
    if (mood >= 4) return 'var(--color-warning)';
    return 'var(--color-danger)';
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const mood = payload[0].value;
      return (
        <div className={styles.tooltip}>
          <p className={styles.tooltipDate}>{payload[0].payload.date}</p>
          <p className={styles.tooltipMood}>
            Mood: <strong>{mood}/10</strong>
          </p>
        </div>
      );
    }
    return null;
  };

  if (chartData.length === 0) {
    return (
      <div className={styles.emptyState}>
        <p>📊 No mood data yet. Start journaling to see your trends!</p>
      </div>
    );
  }

  return (
    <div className={styles.chartContainer}>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="colorMood" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="var(--color-primary)" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="var(--color-primary)" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
          <XAxis 
            dataKey="date" 
            stroke="#718096"
            style={{ fontSize: '0.875rem' }}
          />
          <YAxis 
            domain={[0, 10]} 
            stroke="#718096"
            style={{ fontSize: '0.875rem' }}
            label={{ value: 'Mood Score', angle: -90, position: 'insideLeft', style: { fontSize: '0.875rem', fill: '#718096' } }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area 
            type="monotone" 
            dataKey="mood" 
            stroke="var(--color-primary)" 
            strokeWidth={3}
            fill="url(#colorMood)"
          />
        </AreaChart>
      </ResponsiveContainer>

      <div className={styles.legend}>
        <div className={styles.legendItem}>
          <span className={styles.legendDot} style={{ background: 'var(--color-success)' }}></span>
          <span>Stable (7-10)</span>
        </div>
        <div className={styles.legendItem}>
          <span className={styles.legendDot} style={{ background: 'var(--color-warning)' }}></span>
          <span>Fluctuating (4-6)</span>
        </div>
        <div className={styles.legendItem}>
          <span className={styles.legendDot} style={{ background: 'var(--color-danger)' }}></span>
          <span>Low (1-3)</span>
        </div>
      </div>
    </div>
  );
};

export default MoodChart;
