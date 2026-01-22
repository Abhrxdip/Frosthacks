import React, { ReactNode } from 'react';
import styles from './Layout.module.css';

interface LayoutProps {
  children: ReactNode;
  showNav?: boolean;
}

const Layout: React.FC<LayoutProps> = ({ children, showNav = true }) => {
  return (
    <div className={styles.layout}>
      {showNav && (
        <nav className={styles.nav}>
          <div className={styles.navContent}>
            <h2 className={styles.logo}>✨ MindSpace</h2>
            <div className={styles.navLinks}>
              <a href="/dashboard" className={styles.navLink}>Dashboard</a>
              <a href="/journal" className={styles.navLink}>Journal</a>
              <button 
                onClick={() => {
                  localStorage.removeItem('authToken');
                  window.location.href = '/login';
                }}
                className={styles.logoutBtn}
              >
                Logout
              </button>
            </div>
          </div>
        </nav>
      )}
      <main className={styles.main}>{children}</main>
    </div>
  );
};

export default Layout;
