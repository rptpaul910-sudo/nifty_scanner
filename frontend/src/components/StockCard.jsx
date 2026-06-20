import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const StockCard = ({ stock, rank }) => {
  const isPositive = stock.change_percent >= 0;
  
  const formatNumber = (num) => {
    if (num >= 10000000) return `${(num / 10000000).toFixed(2)} Cr`;
    if (num >= 100000) return `${(num / 100000).toFixed(2)} L`;
    if (num >= 1000) return `${(num / 1000).toFixed(2)} K`;
    return num.toLocaleString();
  };

  const getRankClass = (rank) => {
    if (rank === 1) return 'gold';
    if (rank === 2) return 'silver';
    if (rank === 3) return 'bronze';
    return 'default';
  };

  return (
    <div className={`stock-card ${isPositive ? 'positive' : 'negative'}`}>
      <div className="stock-card-rank">
        <div className={`rank-badge ${getRankClass(rank)}`}>
          {rank}
        </div>
      </div>
      
      <div className="stock-card-header">
        <div className="stock-info">
          <span className="stock-symbol">{stock.symbol}</span>
          <span className="stock-name">{stock.name}</span>
        </div>
      </div>
      
      <div className="stock-card-body">
        <div>
          <div className="stock-card-price">₹{stock.ltp.toFixed(2)}</div>
          <div className="stock-card-change">
            <span className={`stock-change ${isPositive ? 'positive' : 'negative'}`}>
              {isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
              {isPositive ? '+' : ''}{stock.change.toFixed(2)}
            </span>
            <span className={`change-badge ${isPositive ? 'positive' : 'negative'}`}>
              {isPositive ? '+' : ''}{stock.change_percent.toFixed(2)}%
            </span>
          </div>
        </div>
      </div>
      
      <div className="stock-card-stats">
        <div className="stat-item">
          <span className="stat-label">Open</span>
          <span className="stat-value">₹{stock.open.toFixed(2)}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">High</span>
          <span className="stat-value">₹{stock.high.toFixed(2)}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Low</span>
          <span className="stat-value">₹{stock.low.toFixed(2)}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Volume</span>
          <span className="stat-value">{formatNumber(stock.volume)}</span>
        </div>
      </div>
    </div>
  );
};

export default StockCard;
