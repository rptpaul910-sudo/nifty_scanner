import React, { useState, useEffect, useCallback } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  BarChart3, 
  Activity, 
  Layers,
  AlertCircle 
} from 'lucide-react';
import { stocksApi } from '../services/api';
import StockTable from './StockTable';
import StockCard from './StockCard';
import Loader from './Loader';

const Dashboard = ({ refreshTrigger, onMarketStatus }) => {
  const [activeTab, setActiveTab] = useState('gainers');
  const [viewMode, setViewMode] = useState('table');
  const [topGainers, setTopGainers] = useState([]);
  const [topLosers, setTopLosers] = useState([]);
  const [allStocks, setAllStocks] = useState([]);
  const [marketSummary, setMarketSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [marketStatus, setMarketStatus] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const [gainersRes, losersRes, summaryRes] = await Promise.all([
        stocksApi.getTopGainers(10),
        stocksApi.getTopLosers(10),
        stocksApi.getMarketSummary(),
      ]);

      if (gainersRes.success) setTopGainers(gainersRes.data);
      if (losersRes.success) setTopLosers(losersRes.data);
      if (summaryRes.success) setMarketSummary(summaryRes.data);

      // market_status is identical across endpoints (computed server-side from
      // current time), so any one response's value is sufficient.
      const status = gainersRes.market_status || losersRes.market_status || summaryRes.market_status;
      if (status) {
        setMarketStatus(status);
        if (onMarketStatus) onMarketStatus(status);
      }

      setLastUpdated(new Date().toISOString());
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch market data. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData, refreshTrigger]);

  // Auto-refresh every 60 seconds
  useEffect(() => {
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const formatVolume = (vol) => {
    if (vol >= 10000000) return `${(vol / 10000000).toFixed(2)} Cr`;
    if (vol >= 100000) return `${(vol / 100000).toFixed(2)} L`;
    return vol.toLocaleString();
  };

  if (loading && !marketSummary) {
    return <Loader text="Scanning Nifty50 stocks..." />;
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-icon">
          <AlertCircle size={32} />
        </div>
        <h3>Unable to Load Data</h3>
        <p className="error-text">{error}</p>
        <button className="retry-btn" onClick={fetchData}>
          Try Again
        </button>
      </div>
    );
  }

  const currentData = activeTab === 'gainers' ? topGainers : topLosers;

  return (
    <div className="dashboard">
      {/* Summary Cards */}
      {marketSummary && (
        <div className="summary-grid">
          <div className="summary-card gainers">
            <div className="summary-card-header">
              <div className="summary-card-icon">
                <TrendingUp size={22} />
              </div>
              <span className="summary-card-title">Gainers</span>
            </div>
            <div className="summary-card-value">{marketSummary.gainers_count}</div>
            <div className="summary-card-change">
              of {marketSummary.total_stocks} stocks
            </div>
          </div>

          <div className="summary-card losers">
            <div className="summary-card-header">
              <div className="summary-card-icon">
                <TrendingDown size={22} />
              </div>
              <span className="summary-card-title">Losers</span>
            </div>
            <div className="summary-card-value">{marketSummary.losers_count}</div>
            <div className="summary-card-change">
              of {marketSummary.total_stocks} stocks
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-card-header">
              <div className="summary-card-icon">
                <Activity size={22} />
              </div>
              <span className="summary-card-title">Avg Change</span>
            </div>
            <div className="summary-card-value" style={{ 
              color: marketSummary.average_change >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' 
            }}>
              {marketSummary.average_change >= 0 ? '+' : ''}{marketSummary.average_change}%
            </div>
            <div className="summary-card-change">
              {marketSummary.market_sentiment}
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-card-header">
              <div className="summary-card-icon">
                <BarChart3 size={22} />
              </div>
              <span className="summary-card-title">Volume</span>
            </div>
            <div className="summary-card-value">
              {formatVolume(marketSummary.total_volume)}
            </div>
            <div className="summary-card-change">
              Total traded
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="tabs-container">
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'gainers' ? 'active' : ''}`}
            onClick={() => setActiveTab('gainers')}
          >
            <TrendingUp size={16} style={{ marginRight: '0.5rem' }} />
            Top Gainers
          </button>
          <button 
            className={`tab ${activeTab === 'losers' ? 'active' : ''}`}
            onClick={() => setActiveTab('losers')}
          >
            <TrendingDown size={16} style={{ marginRight: '0.5rem' }} />
            Top Losers
          </button>
          <button 
            className={`tab ${viewMode === 'table' ? 'active' : ''}`}
            onClick={() => setViewMode(viewMode === 'table' ? 'cards' : 'table')}
          >
            <Layers size={16} style={{ marginRight: '0.5rem' }} />
            {viewMode === 'table' ? 'Card View' : 'Table View'}
          </button>
        </div>
      </div>

      {/* Content */}
      {loading ? (
        <Loader text="Updating data..." />
      ) : viewMode === 'table' ? (
        <StockTable 
          stocks={currentData}
          title={activeTab === 'gainers' ? 'Top Gainers' : 'Top Losers'}
          icon={activeTab === 'gainers' ? TrendingUp : TrendingDown}
          lastUpdated={lastUpdated}
          marketStatus={marketStatus}
        />
      ) : (
        <div className="stock-cards-grid">
          {currentData.map((stock, index) => (
            <StockCard key={stock.symbol} stock={stock} rank={index + 1} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
