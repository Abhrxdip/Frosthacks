import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '@/hooks/useAuth';
import Button from '@/components/Button/Button';
import Card from '@/components/Card/Card';
import styles from './auth.module.css';

const Login: React.FC = () => {
  const router = useRouter();
  const { login, loading, error } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await login({ email, password });
    if (result.success) {
      router.push('/dashboard');
    }
  };

  const handleDemoLogin = () => {
    // Demo mode - bypass backend with rich sample data
    localStorage.setItem('authToken', 'demo-mode-token');
    router.push('/dashboard');
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authContent}>
        <div className={styles.header}>
          <h1 className={styles.logo}>✨ MindSpace</h1>
          <p className={styles.tagline}>Your private space for mental wellness</p>
        </div>

        <Card>
          <h2 className={styles.title}>Welcome back</h2>
          <p className={styles.subtitle}>Sign in to continue your journey</p>

          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.formGroup}>
              <label htmlFor="email" className={styles.label}>Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className={styles.input}
                placeholder="you@example.com"
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="password" className={styles.label}>Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className={styles.input}
                placeholder="••••••••"
              />
            </div>

            {error && (
              <div className={styles.errorMessage}>
                {error}
              </div>
            )}

            <Button type="submit" disabled={loading} fullWidth>
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>

            <div style={{ margin: '1rem 0', textAlign: 'center', color: '#718096' }}>
              or
            </div>

            <Button variant="outline" onClick={handleDemoLogin} fullWidth>
              🎮 Demo Mode (No Backend Required)
            </Button>
          </form>

          <div className={styles.footer}>
            <p>Don't have an account? <a href="/register" className={styles.link}>Create one</a></p>
          </div>
        </Card>

        <div className={styles.privacyNotice}>
          <p>🔒 Your data is encrypted and completely private</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
