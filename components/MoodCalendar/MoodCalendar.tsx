import React from 'react';
// @ts-ignore
import CalendarHeatmap from 'react-calendar-heatmap';
// @ts-ignore
import 'react-calendar-heatmap/dist/styles.css';
import styles from './MoodCalendar.module.css';

interface MoodEntry {
  date: string;
  count: number; // mood score
}

interface MoodCalendarProps {
  moodHistory: Array<{ date: string; mood: number }>;
}

const MoodCalendar: React.FC<MoodCalendarProps> = ({ moodHistory }) => {
  // Transform mood history to heatmap format
  const heatmapData: MoodEntry[] = moodHistory.map(entry => ({
    date: entry.date.split('T')[0],
    count: entry.mood
  }));

  const today = new Date();
  const sixMonthsAgo = new Date(today);
  sixMonthsAgo.setMonth(today.getMonth() - 6);

  const getColorClass = (value: MoodEntry | undefined) => {
    if (!value || !value.count) return 'color-empty';
    if (value.count >= 8) return 'color-scale-5';
    if (value.count >= 6) return 'color-scale-4';
    if (value.count >= 5) return 'color-scale-3';
    if (value.count >= 3) return 'color-scale-2';
    return 'color-scale-1';
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>6-Month Mood History</h3>
      <div className={styles.heatmapWrapper}>
        <CalendarHeatmap
          startDate={sixMonthsAgo}
          endDate={today}
          values={heatmapData}
          classForValue={(value: any) => getColorClass(value)}
          tooltipDataAttrs={(value: any) => {
            if (!value || !value.date) return {};
            return {
              'data-tip': `${value.date}: Mood ${value.count}/10`
            };
          }}
          showWeekdayLabels={true}
        />
      </div>
      <div className={styles.legend}>
        <span>Less</span>
        <div className={styles.legendBoxes}>
          <div className={`${styles.legendBox} ${styles.level1}`}></div>
          <div className={`${styles.legendBox} ${styles.level2}`}></div>
          <div className={`${styles.legendBox} ${styles.level3}`}></div>
          <div className={`${styles.legendBox} ${styles.level4}`}></div>
          <div className={`${styles.legendBox} ${styles.level5}`}></div>
        </div>
        <span>More</span>
      </div>
    </div>
  );
};

export default MoodCalendar;
