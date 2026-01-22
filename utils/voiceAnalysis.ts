import Meyda from 'meyda';

export interface VoiceAnalysis {
  pitch: number;
  energy: number;
  spectralCentroid: number;
  rms: number;
  zcr: number;
  moodScore: number; // 1-10 based on voice features
  clarity: 'clear' | 'moderate' | 'unclear';
  timestamp: string;
}

export class VoiceAnalyzer {
  private audioContext: AudioContext | null = null;
  private analyzer: any = null;
  private mediaStream: MediaStream | null = null;

  async startAnalysis(stream: MediaStream): Promise<void> {
    this.audioContext = new AudioContext();
    this.mediaStream = stream;
    
    const source = this.audioContext.createMediaStreamSource(stream);
    
    // Initialize Meyda analyzer
    this.analyzer = Meyda.createMeydaAnalyzer({
      audioContext: this.audioContext,
      source: source,
      bufferSize: 512,
      featureExtractors: [
        'rms',
        'energy',
        'spectralCentroid',
        'zcr',
      ],
      callback: (features: any) => {
        // Features are extracted automatically
      }
    });

    this.analyzer.start();
  }

  getCurrentFeatures(): VoiceAnalysis | null {
    if (!this.analyzer) return null;

    const features = this.analyzer.get();
    
    if (!features) return null;

    // Calculate mood score from voice features
    // Higher energy, moderate pitch = better mood
    // Lower energy, irregular patterns = worse mood
    const energyScore = Math.min(features.energy * 100, 10);
    const clarityScore = Math.max(0, 10 - (features.zcr / 100));
    
    const moodScore = Math.round((energyScore * 0.6 + clarityScore * 0.4));
    
    let clarity: 'clear' | 'moderate' | 'unclear' = 'moderate';
    if (features.rms > 0.5) clarity = 'clear';
    else if (features.rms < 0.2) clarity = 'unclear';

    return {
      pitch: features.spectralCentroid || 0,
      energy: features.energy || 0,
      spectralCentroid: features.spectralCentroid || 0,
      rms: features.rms || 0,
      zcr: features.zcr || 0,
      moodScore: Math.max(1, Math.min(10, moodScore)),
      clarity,
      timestamp: new Date().toISOString()
    };
  }

  stopAnalysis(): void {
    if (this.analyzer) {
      this.analyzer.stop();
    }
    if (this.audioContext) {
      this.audioContext.close();
    }
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(track => track.stop());
    }
  }
}

// Simple sentiment analysis for text (VADER-like approach)
export function analyzeSentiment(text: string): number {
  const positiveWords = [
    'happy', 'joy', 'love', 'excellent', 'good', 'great', 'wonderful', 
    'fantastic', 'amazing', 'positive', 'excited', 'grateful', 'blessed',
    'peaceful', 'calm', 'better', 'improved', 'progress', 'success'
  ];
  
  const negativeWords = [
    'sad', 'angry', 'hate', 'bad', 'terrible', 'awful', 'horrible',
    'depressed', 'anxious', 'worried', 'scared', 'lonely', 'hopeless',
    'stressed', 'overwhelmed', 'exhausted', 'tired', 'hurt', 'pain'
  ];

  const words = text.toLowerCase().split(/\s+/);
  let score = 5; // Neutral baseline

  words.forEach(word => {
    if (positiveWords.includes(word)) score += 0.5;
    if (negativeWords.includes(word)) score -= 0.5;
  });

  // Detect negation
  const negationPattern = /(not|no|never|don't|doesn't|didn't|won't|wouldn't|can't|couldn't)\s+(\w+)/gi;
  const matches = text.toLowerCase().match(negationPattern);
  if (matches) {
    score -= matches.length * 0.3;
  }

  // Detect exclamation (enthusiasm)
  const exclamations = (text.match(/!/g) || []).length;
  score += exclamations * 0.2;

  // Detect question marks (uncertainty)
  const questions = (text.match(/\?/g) || []).length;
  if (questions > 2) score -= 0.3;

  return Math.max(1, Math.min(10, Math.round(score)));
}

// Detect if intervention is needed
export function shouldIntervene(moodHistory: Array<{ mood: number; date: string }>): boolean {
  if (moodHistory.length < 5) return false;

  // Get last 7 days
  const recent = moodHistory.slice(-7);
  const avgMood = recent.reduce((sum, entry) => sum + entry.mood, 0) / recent.length;

  // Check for consistent decline
  const isDecline = recent.every((entry, i) => {
    if (i === 0) return true;
    return entry.mood <= recent[i - 1].mood + 1;
  });

  // Trigger intervention if average is low or consistent decline
  return avgMood < 4 || (isDecline && avgMood < 5.5);
}
