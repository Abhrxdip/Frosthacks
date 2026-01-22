import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '@/hooks/useAuth';
import Button from '@/components/Button/Button';
import Card from '@/components/Card/Card';
import styles from './auth.module.css';

const Register: React.FC = () => {
  const router = useRouter();
  const { register, loading, error } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await register({ email, password, confirmPassword });
    if (result.success) {
      router.push('/dashboard');
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authContent}>
        <div className={styles.header}>
          <h1 className={styles.logo}>✨ MindSpace</h1>
          <p className={styles.tagline}>Your private space for mental wellness</p>
        </div>

        <Card>
          <h2 className={styles.title}>Create your account</h2>
          <p className={styles.subtitle}>Start your mental wellness journey today</p>

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
                minLength={8}
                className={styles.input}
                placeholder="••••••••"
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="confirmPassword" className={styles.label}>Confirm Password</label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                minLength={8}
                className={styles.input}
                placeholder="••••••••"
              />
            </div>

            {error && (
              <div className={styles.errorMessage}>
                {error}
              </div>
            )}

            <div className={styles.privacyCheckbox}>
              <p className={styles.privacyText}>
                By creating an account, you agree that your data will be encrypted and kept completely private. 
                We never share your personal information.
              </p>
            </div>

            <Button type="submit" disabled={loading} fullWidth>
              {loading ? 'Creating account...' : 'Create Account'}
            </Button>
          </form>

          <div className={styles.footer}>
            <p>Already have an account? <a href="/login" className={styles.link}>Sign in</a></p>
          </div>
        </Card>

        <div className={styles.privacyNotice}>
          <p>🔒 End-to-end encrypted • 🤐 Completely confidential • 💜 Judgment-free</p>
        </div>
      </div>
    </div>
  );
};

export default Register;
