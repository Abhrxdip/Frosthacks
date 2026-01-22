// Demo data for testing without backend

export const DEMO_TOKEN = 'demo-mode-token';

export const demoMoodHistory = [
  { id: '1', date: new Date(Date.now() - 0 * 24 * 60 * 60 * 1000).toISOString(), mood: 8, source: 'text' },
  { id: '2', date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), mood: 7, source: 'voice' },
  { id: '3', date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), mood: 6, source: 'text' },
  { id: '4', date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), mood: 7, source: 'voice' },
  { id: '5', date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(), mood: 8, source: 'text' },
  { id: '6', date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), mood: 6, source: 'text' },
  { id: '7', date: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString(), mood: 7, source: 'voice' },
  { id: '8', date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(), mood: 5, source: 'text' },
  { id: '9', date: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString(), mood: 6, source: 'voice' },
  { id: '10', date: new Date(Date.now() - 9 * 24 * 60 * 60 * 1000).toISOString(), mood: 7, source: 'text' },
  { id: '11', date: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(), mood: 8, source: 'text' },
  { id: '12', date: new Date(Date.now() - 11 * 24 * 60 * 60 * 1000).toISOString(), mood: 6, source: 'voice' },
  { id: '13', date: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString(), mood: 7, source: 'text' },
  { id: '14', date: new Date(Date.now() - 13 * 24 * 60 * 60 * 1000).toISOString(), mood: 5, source: 'text' },
  { id: '15', date: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000).toISOString(), mood: 6, source: 'voice' },
  { id: '16', date: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(), mood: 8, source: 'text' },
  { id: '17', date: new Date(Date.now() - 16 * 24 * 60 * 60 * 1000).toISOString(), mood: 7, source: 'voice' },
  { id: '18', date: new Date(Date.now() - 17 * 24 * 60 * 60 * 1000).toISOString(), mood: 9, source: 'text' },
  { id: '19', date: new Date(Date.now() - 18 * 24 * 60 * 60 * 1000).toISOString(), mood: 6, source: 'text' },
  { id: '20', date: new Date(Date.now() - 19 * 24 * 60 * 60 * 1000).toISOString(), mood: 7, source: 'voice' },
  { id: '21', date: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString(), mood: 8, source: 'text' },
  { id: '22', date: new Date(Date.now() - 25 * 24 * 60 * 60 * 1000).toISOString(), mood: 5, source: 'text' },
  { id: '23', date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(), mood: 7, source: 'voice' },
  { id: '24', date: new Date(Date.now() - 35 * 24 * 60 * 60 * 1000).toISOString(), mood: 6, source: 'text' },
  { id: '25', date: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000).toISOString(), mood: 8, source: 'text' },
  { id: '26', date: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000).toISOString(), mood: 9, source: 'voice' },
  { id: '27', date: new Date(Date.now() - 50 * 24 * 60 * 60 * 1000).toISOString(), mood: 7, source: 'text' },
  { id: '28', date: new Date(Date.now() - 55 * 24 * 60 * 60 * 1000).toISOString(), mood: 6, source: 'text' },
  { id: '29', date: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000).toISOString(), mood: 8, source: 'voice' },
  { id: '30', date: new Date(Date.now() - 65 * 24 * 60 * 60 * 1000).toISOString(), mood: 7, source: 'text' },
];

export const demoJournalEntries = [
  {
    id: '1',
    date: new Date(Date.now() - 0 * 24 * 60 * 60 * 1000).toISOString(),
    content: 'Had a great day today! Finished my project and felt really accomplished. The weather was perfect for a walk.',
    mood: 8,
    source: 'text'
  },
  {
    id: '2',
    date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    content: 'Feeling good overall. Had some challenges at work but managed to solve them. Looking forward to the weekend.',
    mood: 7,
    source: 'voice'
  },
  {
    id: '3',
    date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    content: 'A bit stressed about upcoming deadlines, but staying positive. Did some yoga which helped a lot.',
    mood: 6,
    source: 'text'
  },
  {
    id: '4',
    date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    content: 'Had a productive meeting today. Feeling motivated and energized. Team collaboration was excellent!',
    mood: 7,
    source: 'voice'
  },
  {
    id: '5',
    date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
    content: 'Amazing day! Received positive feedback on my presentation. Celebrated with friends in the evening.',
    mood: 8,
    source: 'text'
  },
];

export const demoTrendStatus = {
  status: 'stable',
  message: 'Your mood has been stable and positive over the past week',
  avgMood: 7.2
};

export const isDemoMode = () => {
  if (typeof window === 'undefined') return false;
  const token = localStorage.getItem('authToken');
  return token === DEMO_TOKEN;
};

export const getDemoUser = () => ({
  id: 'demo-user',
  email: 'demo@mindspace.app',
  name: 'Demo User'
});
