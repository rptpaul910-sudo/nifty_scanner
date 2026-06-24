import React from 'react';
import { RefreshCw, TrendingUp } from 'lucide-react';

const Header = ({ onRefresh, isLoading, lastUpdated, marketStatus }) => {
  // Instant client-side estimate shown only until the backend's authoritative
  // market_status (IST-based, computed server-side) arrives on first load.
  const estimateMarketOpen = () => {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const day = now.getDay();

    if (day === 0 || day === 6) return false;
    if (hours < 9 || hours > 15) return false;
    if (hours === 9 && minutes < 15) return false;
    if (hours === 15 && minutes > 30) return false;

    return true;
  };

  const marketOpen = marketStatus ? marketStatus.is_open : estimateMarketOpen();
  const statusLabel = marketStatus ? marketStatus.label : (marketOpen ? 'Market Open' : 'Market Closed');

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
          <div className="market-status" title={marketStatus && marketStatus.note ? marketStatus.note : undefined}>
            <span className={`status-dot ${marketOpen ? 'open' : 'closed'}`}></span>
            <span>{statusLabel}</span>
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
