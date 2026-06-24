import React, { useState } from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import { stocksApi } from './services/api';
import './App.css';

function App() {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [marketStatus, setMarketStatus] = useState(null);

  const handleRefresh = async () => {
    try {
      setIsRefreshing(true);
      await stocksApi.refreshData();
      setRefreshTrigger(prev => prev + 1);
    } catch (error) {
      console.error('Refresh error:', error);
    } finally {
      setIsRefreshing(false);
    }
  };

  return (
    <div className="app">
      <Header 
        onRefresh={handleRefresh} 
        isLoading={isRefreshing}
        marketStatus={marketStatus}
      />
      <main className="main-content">
        <Dashboard refreshTrigger={refreshTrigger} onMarketStatus={setMarketStatus} />
      </main>
    </div>
  );
}

export default App;
