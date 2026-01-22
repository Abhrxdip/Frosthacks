import React, { useState, useEffect } from 'react';
import styles from './ResourceBot.module.css';

interface ResourceBotProps {
  show: boolean;
  onDismiss: () => void;
}

const ResourceBot: React.FC<ResourceBotProps> = ({ show, onDismiss }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (show) {
      // Delay appearance for smooth animation
      setTimeout(() => setIsVisible(true), 500);
    } else {
      setIsVisible(false);
    }
  }, [show]);

  if (!show && !isVisible) return null;

  const handleShowResources = () => {
    // Navigate to resources or show modal
    alert('Campus resources:\n\n• Student Counseling Center\n• Wellness Services\n• Peer Support Groups\n• 24/7 Crisis Hotline: 1-800-273-8255');
    onDismiss();
  };

  const handleRemindLater = () => {
    // Set reminder for later (could store in localStorage)
    localStorage.setItem('botReminderDismissed', Date.now().toString());
    onDismiss();
  };

  return (
    <div className={`${styles.overlay} ${isVisible ? styles.visible : ''}`}>
      <div className={`${styles.botContainer} ${isVisible ? styles.slideIn : ''}`}>
        <button onClick={onDismiss} className={styles.closeBtn} aria-label="Close">
          ✕
        </button>
        
        <div className={styles.botAvatar}>💜</div>
        
        <div className={styles.content}>
          <h3>Hey there 👋</h3>
          <p>
            I noticed you've been feeling a bit low recently. 
            You're not alone, and it's completely okay to ask for support.
          </p>
          <p className={styles.subtitle}>
            Would you like to explore some support options?
          </p>
        </div>

        <div className={styles.actions}>
          <button onClick={handleShowResources} className={styles.primaryBtn}>
            Show Campus Resources
          </button>
          <button onClick={handleRemindLater} className={styles.secondaryBtn}>
            Remind Me Later
          </button>
          <button onClick={onDismiss} className={styles.tertiaryBtn}>
            I'm Okay For Now
          </button>
        </div>

        <div className={styles.footer}>
          <p>This is just a friendly check-in. Take care of yourself 💙</p>
        </div>
      </div>
    </div>
  );
};

export default ResourceBot;
