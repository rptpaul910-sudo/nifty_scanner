import React from 'react';
import { TrendingUp, TrendingDown, ArrowUp, ArrowDown } from 'lucide-react';

const StockTable = ({ stocks, title, icon: Icon, lastUpdated }) => {
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
    <div className="stock-table-container">
      <div className="stock-table-header">
        <h2>
          {Icon && <Icon size={24} />}
          {title}
        </h2>
        {lastUpdated && (
          <span className="last-updated">
            Last updated: {new Date(lastUpdated).toLocaleTimeString()}
          </span>
        )}
      </div>
      
      <table className="stock-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Stock</th>
            <th>LTP</th>
            <th>Change</th>
            <th>% Change</th>
            <th>Open</th>
            <th>High</th>
            <th>Low</th>
            <th>Volume</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock, index) => {
            const isPositive = stock.change_percent >= 0;
            return (
              <tr key={stock.symbol}>
                <td>
                  <div className={`rank-badge ${getRankClass(index + 1)}`}>
                    {index + 1}
                  </div>
                </td>
                <td>
                  <div className="stock-info">
                    <span className="stock-symbol">{stock.symbol}</span>
                    <span className="stock-name">{stock.name}</span>
                  </div>
                </td>
                <td className="stock-price">₹{stock.ltp.toFixed(2)}</td>
                <td>
                  <span className={`stock-change ${isPositive ? 'positive' : 'negative'}`}>
                    {isPositive ? <ArrowUp size={14} /> : <ArrowDown size={14} />}
                    {isPositive ? '+' : ''}₹{stock.change.toFixed(2)}
                  </span>
                </td>
                <td>
                  <span className={`change-badge ${isPositive ? 'positive' : 'negative'}`}>
                    {isPositive ? '+' : ''}{stock.change_percent.toFixed(2)}%
                  </span>
                </td>
                <td>₹{stock.open.toFixed(2)}</td>
                <td>₹{stock.high.toFixed(2)}</td>
                <td>₹{stock.low.toFixed(2)}</td>
                <td className="volume">{formatNumber(stock.volume)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default StockTable;
