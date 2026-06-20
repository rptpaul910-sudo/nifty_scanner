import React from 'react';
import { RefreshCw, TrendingUp } from 'lucide-react';

const Header = ({ onRefresh, isLoading, lastUpdated }) => {
  const isMarketOpen = () => {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const day = now.getDay();
    
    // Market hours: Mon-Fri, 9:15 AM - 3:30 PM IST
    if (day === 0 || day === 6) return false;
    if (hours < 9 || hours > 15) return false;
    if (hours === 9 && minutes < 15) return false;
    if (hours === 15 && minutes > 30) return false;
    
    return true;
  };

  const marketOpen = isMarketOpen();

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <div className="logo-icon">
            <TrendingUp size={24} />
          </div>
          <div className="logo-text">
            <h1>Nifty50 Scanner</h1>
            <span>Real-time Market Analysis</span>
          </div>
        </div>
        
        <div className="header-actions">
          <div className="market-status">
            <span className={`status-dot ${marketOpen ? 'open' : 'closed'}`}></span>
            <span>{marketOpen ? 'Market Open' : 'Market Closed'}</span>
          </div>
          
          <button 
            className={`refresh-btn ${isLoading ? 'loading' : ''}`}
            onClick={onRefresh}
            disabled={isLoading}
          >
            <RefreshCw size={18} />
            {isLoading ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
