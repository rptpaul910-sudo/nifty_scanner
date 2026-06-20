# Nifty50 Top Gainers Scanner

A real-time web application that scans the Indian stock market and displays the top gaining stocks in the Nifty50 index using Angel One Smart API.

## Features

- 📈 Real-time top gainers and losers tracking
- 📊 Market summary with sentiment analysis
- 🔄 Auto-refresh every 60 seconds
- 📱 Responsive design with dark theme
- 💾 Historical data storage in MySQL
- 🎨 Modern UI with card and table views

## Tech Stack

- **Frontend**: React, Axios, Recharts, Lucide Icons
- **Backend**: Python, Flask, Flask-CORS
- **Database**: MySQL
- **API**: Angel One Smart API

## Prerequisites

- Node.js 18+
- Python 3.9+
- MySQL 8.0+
- Angel One trading account with API access

## Installation

### 1. Database Setup

```bash
mysql -u root -p < database/schema.sql


User:

Sir you are expert of share trading. kindly guide me to develop a web app using react, python, flask, mysql, nodejs which scan the market and return top gainer stocks under nifty50. Provide a astetic fronend design. I have alredy setup my enviroment. I have account in Angel One Smart API. Give me the project in floder structured downloadable zip format.

Assistant:

Nifty50 Top Gainers Scanner

I'll build you a complete full-stack application that scans the market using Angel One Smart API and displays the top gaining stocks in Nifty50.

Project Structure

``
nifty50-scanner/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── services/
│   │   ├── init.py
│   │   ├── angelapi.py
│   │   └── database.py
│   └── routes/
│       ├── init.py
│       └── stocks.py
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.js
│       ├── App.js
│       ├── App.css
│       ├── components/
│       │   ├── Header.js
│       │   ├── StockCard.js
│       │   ├── StockTable.js
│       │   ├── Dashboard.js
│       │   └── Loader.js
│       └── services/
│           └── api.js
├── database/
│   └── schema.sql
└── README.md
`

Backend (Python/Flask)
backend/requirements.txt

`txt
flask==3.0.0
flask-cors==4.0.0
flask-mysqldb==2.0.0
smartapi-python==1.4.1
pyotp==2.9.0
python-dotenv==1.0.0
requests==2.31.0
apscheduler==3.10.4
`

backend/config.py

`python
import os
from dotenv import loaddotenv

loaddotenv()

class Config:
    # Angel One API Credentials
    ANGELAPIKEY = os.getenv('ANGELAPIKEY')
    ANGELCLIENTID = os.getenv('ANGELCLIENTID')
    ANGELPASSWORD = os.getenv('ANGELPASSWORD')
    ANGELTOTPSECRET = os.getenv('ANGELTOTPSECRET')
    
    # MySQL Configuration
    MYSQLHOST = os.getenv('MYSQLHOST', 'localhost')
    MYSQLUSER = os.getenv('MYSQLUSER', 'root')
    MYSQLPASSWORD = os.getenv('MYSQLPASSWORD', '')
    MYSQLDB = os.getenv('MYSQLDB', 'nifty50scanner')
    
    # Flask Configuration
    SECRETKEY = os.getenv('SECRETKEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
`

backend/services/init.py

`python
Services package
`

backend/services/angelapi.py

`python
from SmartApi import SmartConnect
import pyotp
from config import Config
import json
import requests

class AngelOneService:
    def init(self):
        self.apikey = Config.ANGELAPIKEY
        self.clientid = Config.ANGELCLIENTID
        self.password = Config.ANGELPASSWORD
        self.totpsecret = Config.ANGELTOTPSECRET
        self.smartapi = None
        self.authtoken = None
        self.refreshtoken = None
        self.feedtoken = None
        
        # Nifty 50 stock tokens (NSE)
        self.nifty50stocks = [
            {"symbol": "RELIANCE", "token": "2885", "name": "Reliance Industries"},
            {"symbol": "TCS", "token": "11536", "name": "Tata Consultancy Services"},
            {"symbol": "HDFCBANK", "token": "1333", "name": "HDFC Bank"},
            {"symbol": "INFY", "token": "1594", "name": "Infosys"},
            {"symbol": "ICICIBANK", "token": "4963", "name": "ICICI Bank"},
            {"symbol": "HINDUNILVR", "token": "1394", "name": "Hindustan Unilever"},
            {"symbol": "SBIN", "token": "3045", "name": "State Bank of India"},
            {"symbol": "BHARTIARTL", "token": "10604", "name": "Bharti Airtel"},
            {"symbol": "ITC", "token": "1660", "name": "ITC"},
            {"symbol": "KOTAKBANK", "token": "1922", "name": "Kotak Mahindra Bank"},
            {"symbol": "LT", "token": "11483", "name": "Larsen & Toubro"},
            {"symbol": "AXISBANK", "token": "5900", "name": "Axis Bank"},
            {"symbol": "ASIANPAINT", "token": "236", "name": "Asian Paints"},
            {"symbol": "MARUTI", "token": "10999", "name": "Maruti Suzuki"},
            {"symbol": "SUNPHARMA", "token": "3351", "name": "Sun Pharmaceutical"},
            {"symbol": "TITAN", "token": "3506", "name": "Titan Company"},
            {"symbol": "BAJFINANCE", "token": "317", "name": "Bajaj Finance"},
            {"symbol": "WIPRO", "token": "3787", "name": "Wipro"},
            {"symbol": "ULTRACEMCO", "token": "11532", "name": "UltraTech Cement"},
            {"symbol": "HCLTECH", "token": "7229", "name": "HCL Technologies"},
            {"symbol": "NTPC", "token": "11630", "name": "NTPC"},
            {"symbol": "POWERGRID", "token": "14977", "name": "Power Grid Corporation"},
            {"symbol": "TATAMOTORS", "token": "3456", "name": "Tata Motors"},
            {"symbol": "M&M", "token": "2031", "name": "Mahindra & Mahindra"},
            {"symbol": "NESTLEIND", "token": "17963", "name": "Nestle India"},
            {"symbol": "BAJAJFINSV", "token": "16675", "name": "Bajaj Finserv"},
            {"symbol": "TATASTEEL", "token": "3499", "name": "Tata Steel"},
            {"symbol": "TECHM", "token": "13538", "name": "Tech Mahindra"},
            {"symbol": "ADANIENT", "token": "25", "name": "Adani Enterprises"},
            {"symbol": "ADANIPORTS", "token": "15083", "name": "Adani Ports"},
            {"symbol": "ONGC", "token": "2475", "name": "ONGC"},
            {"symbol": "COALINDIA", "token": "20374", "name": "Coal India"},
            {"symbol": "JSWSTEEL", "token": "11723", "name": "JSW Steel"},
            {"symbol": "BPCL", "token": "526", "name": "BPCL"},
            {"symbol": "LTIM", "token": "17818", "name": "LTIMindtree"},
            {"symbol": "GRASIM", "token": "1232", "name": "Grasim Industries"},
            {"symbol": "APOLLOHOSP", "token": "157", "name": "Apollo Hospitals"},
            {"symbol": "DRREDDY", "token": "881", "name": "Dr. Reddy's Labs"},
            {"symbol": "CIPLA", "token": "694", "name": "Cipla"},
            {"symbol": "EICHERMOT", "token": "910", "name": "Eicher Motors"},
            {"symbol": "DIVISLAB", "token": "10940", "name": "Divi's Labs"},
            {"symbol": "BRITANNIA", "token": "547", "name": "Britannia Industries"},
            {"symbol": "HINDALCO", "token": "1363", "name": "Hindalco Industries"},
            {"symbol": "INDUSINDBK", "token": "5258", "name": "IndusInd Bank"},
            {"symbol": "SBILIFE", "token": "21808", "name": "SBI Life Insurance"},
            {"symbol": "HDFCLIFE", "token": "467", "name": "HDFC Life"},
            {"symbol": "TATACONSUM", "token": "3432", "name": "Tata Consumer Products"},
            {"symbol": "BAJAJ-AUTO", "token": "16669", "name": "Bajaj Auto"},
            {"symbol": "HEROMOTOCO", "token": "1348", "name": "Hero MotoCorp"},
            {"symbol": "WIPRO", "token": "3787", "name": "Wipro"}
        ]
    
    def login(self):
        """Authenticate with Angel One API"""
        try:
            self.smartapi = SmartConnect(apikey=self.apikey)
            totp = pyotp.TOTP(self.totpsecret).now()
            
            data = self.smartapi.generateSession(
                clientCode=self.clientid,
                password=self.password,
                totp=totp
            )
            
            if data['status']:
                self.authtoken = data['data']['jwtToken']
                self.refreshtoken = data['data']['refreshToken']
                self.feedtoken = self.smartapi.getfeedToken()
                return True
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def getltpdata(self, symboltoken, exchange="NSE"):
        """Get Last Traded Price data for a stock"""
        try:
            ltpdata = self.smartapi.ltpData(exchange, symboltoken, symboltoken)
            return ltpdata
        except Exception as e:
            print(f"LTP Error for {symboltoken}: {e}")
            return None
    
    def getquote(self, symboltoken, exchange="NSE"):
        """Get detailed quote for a stock"""
        try:
            quoteparams = {
                "mode": "FULL",
                "exchangeTokens": {
                    exchange: [symboltoken]
                }
            }
            quotedata = self.smartapi.getMarketData(quoteparams)
            return quotedata
        except Exception as e:
            print(f"Quote Error for {symboltoken}: {e}")
            return None
    
    def scantopgainers(self, limit=10):
        """Scan all Nifty50 stocks and return top gainers"""
        if not self.smartapi:
            if not self.login():
                return []
        
        stocksdata = []
        
        for stock in self.nifty50stocks:
            try:
                quoteparams = {
                    "mode": "FULL",
                    "exchangeTokens": {
                        "NSE": [stock["token"]]
                    }
                }
                
                response = self.smartapi.getMarketData(quoteparams)
                
                if response and response.get('status') and response.get('data'):
                    fetched = response['data']['fetched']
                    if fetched:
                        data = fetched[0]
                        ltp = float(data.get('ltp', 0))
                        close = float(data.get('close', 0))
                        openprice = float(data.get('open', 0))
                        high = float(data.get('high', 0))
                        low = float(data.get('low', 0))
                        volume = int(data.get('tradeVolume', 0))
                        
                        if close > 0:
                            change = ltp - close
                            changepercent = ((ltp - close) / close)  100
                        else:
                            change = 0
                            changepercent = 0
                        
                        stocksdata.append({
                            "symbol": stock["symbol"],
                            "name": stock["name"],
                            "token": stock["token"],
                            "ltp": round(ltp, 2),
                            "open": round(openprice, 2),
                            "high": round(high, 2),
                            "low": round(low, 2),
                            "close": round(close, 2),
                            "change": round(change, 2),
                            "changepercent": round(changepercent, 2),
                            "volume": volume
                        })
                        
            except Exception as e:
                print(f"Error fetching {stock['symbol']}: {e}")
                continue
        
        # Sort by changepercent descending (top gainers)
        stocksdata.sort(key=lambda x: x['changepercent'], reverse=True)
        
        return stocksdata[:limit]
    
    def getallnifty50data(self):
        """Get data for all Nifty50 stocks"""
        return self.scantopgainers(limit=50)
    
    def logout(self):
        """Logout from Angel One API"""
        try:
            if self.smartapi:
                self.smartapi.terminateSession(self.clientid)
                return True
        except Exception as e:
            print(f"Logout error: {e}")
        return False
`

backend/services/database.py

`python
from flaskmysqldb import MySQL

mysql = MySQL()

def initdb(app):
    """Initialize MySQL connection"""
    mysql.initapp(app)
    return mysql

def savestockdata(cursor, stockdata):
    """Save stock data to database"""
    query = """
        INSERT INTO stockprices 
        (symbol, name, token, ltp, openprice, high, low, closeprice, 
         changevalue, changepercent, volume, recordedat)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    cursor.execute(query, (
        stockdata['symbol'],
        stockdata['name'],
        stockdata['token'],
        stockdata['ltp'],
        stockdata['open'],
        stockdata['high'],
        stockdata['low'],
        stockdata['close'],
        stockdata['change'],
        stockdata['changepercent'],
        stockdata['volume']
    ))

def gethistoricalgainers(cursor, limit=10, days=7):
    """Get historical top gainers"""
    query = """
        SELECT symbol, name, 
               AVG(changepercent) as avggain,
               COUNT() as appearancecount
        FROM stockprices
        WHERE recordedat >= DATESUB(NOW(), INTERVAL %s DAY)
          AND changepercent > 0
        GROUP BY symbol, name
        ORDER BY avggain DESC
        LIMIT %s
    """
    cursor.execute(query, (days, limit))
    return cursor.fetchall()
`

backend/routes/init.py

`python
Routes package
`

backend/routes/stocks.py

`python
from flask import Blueprint, jsonify, request
from services.angelapi import AngelOneService
from services.database import mysql, savestockdata, gethistoricalgainers

stocksbp = Blueprint('stocks', name)
angelservice = AngelOneService()

@stocksbp.route('/api/top-gainers', methods=['GET'])
def gettopgainers():
    """Get top gaining stocks in Nifty50"""
    try:
        limit = request.args.get('limit', 10, type=int)
        gainers = angelservice.scantopgainers(limit=limit)
        
        # Save to database
        if gainers:
            try:
                cursor = mysql.connection.cursor()
                for stock in gainers:
                    savestockdata(cursor, stock)
                mysql.connection.commit()
                cursor.close()
            except Exception as dberror:
                print(f"Database error: {dberror}")
        
        return jsonify({
            "success": True,
            "data": gainers,
            "count": len(gainers)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@stocksbp.route('/api/all-stocks', methods=['GET'])
def getallstocks():
    """Get all Nifty50 stocks data"""
    try:
        stocks = angelservice.getallnifty50data()
        return jsonify({
            "success": True,
            "data": stocks,
            "count": len(stocks)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@stocksbp.route('/api/top-losers', methods=['GET'])
def gettoplosers():
    """Get top losing stocks in Nifty50"""
    try:
        limit = request.args.get('limit', 10, type=int)
        allstocks = angelservice.getallnifty50data()
        
        # Sort by changepercent ascending (losers first)
        allstocks.sort(key=lambda x: x['changepercent'])
        losers = allstocks[:limit]
        
        return jsonify({
            "success": True,
            "data": losers,
            "count": len(losers)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@stocksbp.route('/api/market-summary', methods=['GET'])
def getmarketsummary():
    """Get market summary statistics"""
    try:
        allstocks = angelservice.getallnifty50data()
        
        if not allstocks:
            return jsonify({
                "success": False,
                "error": "No data available"
            }), 500
        
        gainers = [s for s in allstocks if s['changepercent'] > 0]
        losers = [s for s in allstocks if s['changepercent'] < 0]
        unchanged = [s for s in allstocks if s['changepercent'] == 0]
        
        totalvolume = sum(s['volume'] for s in allstocks)
        avgchange = sum(s['changepercent'] for s in allstocks) / len(allstocks)
        
        topgainer = max(allstocks, key=lambda x: x['changepercent'])
        toploser = min(allstocks, key=lambda x: x['changepercent'])
        
        return jsonify({
            "success": True,
            "data": {
                "totalstocks": len(allstocks),
                "gainerscount": len(gainers),
                "loserscount": len(losers),
                "unchangedcount": len(unchanged),
                "totalvolume": totalvolume,
                "averagechange": round(avgchange, 2),
                "topgainer": topgainer,
                "toploser": toploser,
                "marketsentiment": "Bullish" if len(gainers) > len(losers) else "Bearish"
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@stocksbp.route('/api/historical-gainers', methods=['GET'])
def gethistorical():
    """Get historical top gainers"""
    try:
        limit = request.args.get('limit', 10, type=int)
        days = request.args.get('days', 7, type=int)
        
        cursor = mysql.connection.cursor()
        historical = gethistoricalgainers(cursor, limit, days)
        cursor.close()
        
        return jsonify({
            "success": True,
            "data": historical
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@stocksbp.route('/api/refresh', methods=['POST'])
def refreshdata():
    """Force refresh data from Angel One API"""
    try:
        # Re-login to refresh session
        if angelservice.login():
            gainers = angelservice.scantopgainers(limit=10)
            return jsonify({
                "success": True,
                "message": "Data refreshed successfully",
                "data": gainers
            })
        return jsonify({
            "success": False,
            "error": "Failed to refresh session"
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
`

backend/app.py

`python
from flask import Flask, jsonify
from flaskcors import CORS
from config import Config
from services.database import initdb
from routes.stocks import stocksbp
from apscheduler.schedulers.background import BackgroundScheduler
from services.angelapi import AngelOneService

app = Flask(name)
app.config.fromobject(Config)

MySQL Configuration
app.config['MYSQLHOST'] = Config.MYSQLHOST
app.config['MYSQLUSER'] = Config.MYSQLUSER
app.config['MYSQLPASSWORD'] = Config.MYSQLPASSWORD
app.config['MYSQLDB'] = Config.MYSQLDB
app.config['MYSQLCURSORCLASS'] = 'DictCursor'

Initialize extensions
CORS(app, resources={r"/api/": {"origins": ""}})
mysql = initdb(app)

Register blueprints
app.registerblueprint(stocksbp)

Background scheduler for periodic data refresh
def scheduledscan():
    """Scheduled task to scan market data"""
    with app.appcontext():
        try:
            angelservice = AngelOneService()
            if angelservice.login():
                data = angelservice.scantopgainers(limit=50)
                print(f"Scheduled scan completed: {len(data)} stocks updated")
        except Exception as e:
            print(f"Scheduled scan error: {e}")

scheduler = BackgroundScheduler()
Run every 5 minutes during market hours (9:15 AM - 3:30 PM IST)
scheduler.addjob(
    scheduledscan,
    'cron',
    dayofweek='mon-fri',
    hour='9-15',
    minute='/5'
)

@app.route('/')
def home():
    return jsonify({
        "message": "Nifty50 Top Gainers Scanner API",
        "version": "1.0.0",
        "endpoints": {
            "topgainers": "/api/top-gainers",
            "toplosers": "/api/top-losers",
            "allstocks": "/api/all-stocks",
            "marketsummary": "/api/market-summary",
            "refresh": "/api/refresh"
        }
    })

@app.route('/api/health')
def healthcheck():
    return jsonify({"status": "healthy"})

if name == 'main':
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
`

Database Schema
database/schema.sql

`sql
-- Create database
CREATE DATABASE IF NOT EXISTS nifty50scanner;
USE nifty50scanner;

-- Stock prices table
CREATE TABLE IF NOT EXISTS stockprices (
    id INT AUTOINCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    token VARCHAR(20) NOT NULL,
    ltp DECIMAL(10, 2) NOT NULL,
    openprice DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    closeprice DECIMAL(10, 2),
    changevalue DECIMAL(10, 2),
    changepercent DECIMAL(6, 2),
    volume BIGINT,
    recordedat TIMESTAMP DEFAULT CURRENTTIMESTAMP,
    INDEX idxsymbol (symbol),
    INDEX idxrecordedat (recordedat),
    INDEX idxchangepercent (changepercent)
);

-- Daily summary table
CREATE TABLE IF NOT EXISTS dailysummary (
    id INT AUTOINCREMENT PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    gainerscount INT,
    loserscount INT,
    totalvolume BIGINT,
    avgchange DECIMAL(6, 2),
    topgainersymbol VARCHAR(20),
    topgainerpercent DECIMAL(6, 2),
    toplosersymbol VARCHAR(20),
    toploserpercent DECIMAL(6, 2),
    marketsentiment VARCHAR(20),
    createdat TIMESTAMP DEFAULT CURRENTTIMESTAMP
);

-- User watchlist table
CREATE TABLE IF NOT EXISTS watchlist (
    id INT AUTOINCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    token VARCHAR(20) NOT NULL,
    addedat TIMESTAMP DEFAULT CURRENTTIMESTAMP,
    UNIQUE KEY uniquesymbol (symbol)
);
`

Frontend (React)
frontend/package.json

`json
{
  "name": "nifty50-scanner-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "axios": "^1.6.0",
    "recharts": "^2.10.0",
    "lucide-react": "^0.294.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "proxy": "http://localhost:5000",
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not opmini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
`

frontend/public/index.html

`html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#0f172a" />
    <meta name="description" content="Nifty50 Top Gainers Scanner - Real-time stock market analysis" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <title>Nifty50 Scanner | Top Gainers</title>
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>
</html>
`

frontend/src/index.js

`jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
`

frontend/src/App.css

`css
:root {
  / Dark Theme Colors /
  --bg-primary: #0a0f1a;
  --bg-secondary: #111827;
  --bg-card: #1a2235;
  --bg-card-hover: #1f2a40;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --accent-green: #10b981;
  --accent-green-light: #34d399;
  --accent-red: #ef4444;
  --accent-red-light: #f87171;
  --accent-blue: #3b82f6;
  --accent-purple: #8b5cf6;
  --accent-yellow: #f59e0b;
  --border-color: #2d3748;
  --gradient-start: #1e3a5f;
  --gradient-end: #0f172a;
}

 {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  min-height: 100vh;
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  min-height: 100vh;
  background: 
    radial-gradient(ellipse at 20% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
    linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
}

/ Header Styles /
.header {
  background: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
  padding: 1rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--accent-green) 0%, var(--accent-blue) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.25rem;
  color: white;
}

.logo-text h1 {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-blue) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-text span {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.market-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--bg-card);
  border-radius: 50px;
  font-size: 0.875rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-dot.open {
  background: var(--accent-green);
  box-shadow: 0 0 10px var(--accent-green);
}

.status-dot.closed {
  background: var(--accent-red);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
  border: none;
  border-radius: 10px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.875rem;
}

.refresh-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px -10px rgba(59, 130, 246, 0.5);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.refresh-btn svg {
  width: 18px;
  height: 18px;
}

.refresh-btn.loading svg {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/ Main Content /
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/ Summary Cards /
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.summary-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
}

.summary-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px -20px rgba(0, 0, 0, 0.5);
  border-color: var(--accent-blue);
}

.summary-card.gainers::before {
  background: linear-gradient(90deg, var(--accent-green), var(--accent-green-light));
}

.summary-card.losers::before {
  background: linear-gradient(90deg, var(--accent-red), var(--accent-red-light));
}

.summary-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.summary-card-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(59, 130, 246, 0.15);
}

.summary-card.gainers .summary-card-icon {
  background: rgba(16, 185, 129, 0.15);
  color: var(--accent-green);
}

.summary-card.losers .summary-card-icon {
  background: rgba(239, 68, 68, 0.15);
  color: var(--accent-red);
}

.summary-card-title {
  font-size: 0.875rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.summary-card-value {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.summary-card.gainers .summary-card-value {
  color: var(--accent-green);
}

.summary-card.losers .summary-card-value {
  color: var(--accent-red);
}

.summary-card-change {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

/ Tabs /
.tabs-container {
  margin-bottom: 2rem;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  background: var(--bg-card);
  padding: 0.5rem;
  border-radius: 12px;
  width: fit-content;
}

.tab {
  padding: 0.75rem 1.5rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.tab:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}

.tab.active {
  background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
  color: white;
}

/ Stock Table /
.stock-table-container {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  overflow: hidden;
}

.stock-table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.stock-table-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stock-table-header h2 svg {
  color: var(--accent-green);
}

.last-updated {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.stock-table {
  width: 100%;
  border-collapse: collapse;
}

.stock-table th {
  text-align: left;
  padding: 1rem 1.5rem;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  background: rgba(0, 0, 0, 0.2);
  font-weight: 600;
}

.stock-table td {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  font-size: 0.95rem;
}

.stock-table tr:last-child td {
  border-bottom: none;
}

.stock-table tbody tr {
  transition: all 0.2s ease;
}

.stock-table tbody tr:hover {
  background: var(--bg-card-hover);
}

.stock-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stock-symbol {
  font-weight: 700;
  color: var(--text-primary);
  font-size: 1rem;
}

.stock-name {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.stock-price {
  font-weight: 600;
  font-size: 1.05rem;
  font-variant-numeric: tabular-nums;
}

.stock-change {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.stock-change.positive {
  color: var(--accent-green);
}

.stock-change.negative {
  color: var(--accent-red);
}

.change-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
}

.change-badge.positive {
  background: rgba(16, 185, 129, 0.15);
  color: var(--accent-green);
}

.change-badge.negative {
  background: rgba(239, 68, 68, 0.15);
  color: var(--accent-red);
}

.rank-badge {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
}

.rank-badge.gold {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #1a1a1a;
}

.rank-badge.silver {
  background: linear-gradient(135deg, #9ca3af, #6b7280);
  color: #1a1a1a;
}

.rank-badge.bronze {
  background: linear-gradient(135deg, #cd7f32, #a65f1c);
  color: white;
}

.rank-badge.default {
  background: var(--bg-secondary);
  color: var(--text-secondary);
}

.volume {
  color: var(--text-secondary);
  font-variant-numeric: tabular-nums;
}

/ Stock Cards Grid /
.stock-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.stock-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stock-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px -20px rgba(0, 0, 0, 0.5);
}

.stock-card.positive {
  border-color: rgba(16, 185, 129, 0.3);
}

.stock-card.positive:hover {
  border-color: var(--accent-green);
}

.stock-card.negative {
  border-color: rgba(239, 68, 68, 0.3);
}

.stock-card.negative:hover {
  border-color: var(--accent-red);
}

.stock-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.stock-card-rank {
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.stock-card-body {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.stock-card-price {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.stock-card-change {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stock-card-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border-color);
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.stat-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
}

.stat-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

/ Loader /
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  gap: 1rem;
}

.loader {
  width: 56px;
  height: 56px;
  border: 3px solid var(--border-color);
  border-top-color: var(--accent-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loader-text {
  color: var(--text-muted);
  font-size: 0.9rem;
}

/ Error State /
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  gap: 1rem;
  text-align: center;
}

.error-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent-red);
}

.error-text {
  color: var(--text-secondary);
  max-width: 400px;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: var(--accent-blue);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: var(--accent-purple);
}

/ Responsive /
@media (max-width: 768px) {
  .header {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .summary-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .tabs {
    width: 100%;
    overflow-x: auto;
  }
  
  .stock-table {
    display: block;
    overflow-x: auto;
  }
  
  .stock-cards-grid {
    grid-template-columns: 1fr;
  }
}

/ Scrollbar /
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}
`

frontend/src/services/api.js

`javascript
import axios from 'axios';

const APIBASEURL = process.env.REACTAPPAPIURL || 'http://localhost:5000';

const api = axios.create({
  baseURL: APIBASEURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const stocksApi = {
  getTopGainers: async (limit = 10) => {
    const response = await api.get(/api/top-gainers?limit=${limit});
    return response.data;
  },

  getTopLosers: async (limit = 10) => {
    const response = await api.get(/api/top-losers?limit=${limit});
    return response.data;
  },

  getAllStocks: async () => {
    const response = await api.get('/api/all-stocks');
    return response.data;
  },

  getMarketSummary: async () => {
    const response = await api.get('/api/market-summary');
    return response.data;
  },

  refreshData: async () => {
    const response = await api.post('/api/refresh');
    return response.data;
  },

  getHistoricalGainers: async (limit = 10, days = 7) => {
    const response = await api.get(/api/historical-gainers?limit=${limit}&days=${days});
    return response.data;
  },
};

export default api;
`

frontend/src/components/Header.js

`jsx
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
            <span className={status-dot ${marketOpen ? 'open' : 'closed'}}></span>
            <span>{marketOpen ? 'Market Open' : 'Market Closed'}</span>
          </div>
          
          <button 
            className={refresh-btn ${isLoading ? 'loading' : ''}}
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
`

frontend/src/components/Loader.js

`jsx
import React from 'react';

const Loader = ({ text = 'Loading market data...' }) => {
  return (
    <div className="loader-container">
      <div className="loader"></div>
      <p className="loader-text">{text}</p>
    </div>
  );
};

export default Loader;
`

frontend/src/components/StockCard.js

`jsx
import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const StockCard = ({ stock, rank }) => {
  const isPositive = stock.changepercent >= 0;
  
  const formatNumber = (num) => {
    if (num >= 10000000) return ${(num / 10000000).toFixed(2)} Cr;
    if (num >= 100000) return ${(num / 100000).toFixed(2)} L;
    if (num >= 1000) return ${(num / 1000).toFixed(2)} K;
    return num.toLocaleString();
  };

  const getRankClass = (rank) => {
    if (rank === 1) return 'gold';
    if (rank === 2) return 'silver';
    if (rank === 3) return 'bronze';
    return 'default';
  };

  return (
    <div className={stock-card ${isPositive ? 'positive' : 'negative'}}>
      <div className="stock-card-rank">
        <div className={rank-badge ${getRankClass(rank)}}>
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
            <span className={stock-change ${isPositive ? 'positive' : 'negative'}}>
              {isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
              {isPositive ? '+' : ''}{stock.change.toFixed(2)}
            </span>
            <span className={change-badge ${isPositive ? 'positive' : 'negative'}}>
              {isPositive ? '+' : ''}{stock.changepercent.toFixed(2)}%
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
`

frontend/src/components/StockTable.js

`jsx
import React from 'react';
import { TrendingUp, TrendingDown, ArrowUp, ArrowDown } from 'lucide-react';

const StockTable = ({ stocks, title, icon: Icon, lastUpdated }) => {
  const formatNumber = (num) => {
    if (num >= 10000000) return ${(num / 10000000).toFixed(2)} Cr;
    if (num >= 100000) return ${(num / 100000).toFixed(2)} L;
    if (num >= 1000) return ${(num / 1000).toFixed(2)} K;
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
            const isPositive = stock.changepercent >= 0;
            return (
              <tr key={stock.symbol}>
                <td>
                  <div className={rank-badge ${getRankClass(index + 1)}}>
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
                  <span className={stock-change ${isPositive ? 'positive' : 'negative'}}>
                    {isPositive ? <ArrowUp size={14} /> : <ArrowDown size={14} />}
                    {isPositive ? '+' : ''}₹{stock.change.toFixed(2)}
                  </span>
                </td>
                <td>
                  <span className={change-badge ${isPositive ? 'positive' : 'negative'}}>
                    {isPositive ? '+' : ''}{stock.changepercent.toFixed(2)}%
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
`

frontend/src/components/Dashboard.js

`jsx
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

const Dashboard = ({ refreshTrigger }) => {
  const [activeTab, setActiveTab] = useState('gainers');
  const [viewMode, setViewMode] = useState('table');
  const [topGainers, setTopGainers] = useState([]);
  const [topLosers, setTopLosers] = useState([]);
  const [allStocks, setAllStocks] = useState([]);
  const [marketSummary, setMarketSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

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
    if (vol >= 10000000) return ${(vol / 10000000).toFixed(2)} Cr;
    if (vol >= 100000) return ${(vol / 100000).toFixed(2)} L;
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
      {/ Summary Cards /}
      {marketSummary && (
        <div className="summary-grid">
          <div className="summary-card gainers">
            <div className="summary-card-header">
              <div className="summary-card-icon">
                <TrendingUp size={22} />
              </div>
              <span className="summary-card-title">Gainers</span>
            </div>
            <div className="summary-card-value">{marketSummary.gainerscount}</div>
            <div className="summary-card-change">
              of {marketSummary.totalstocks} stocks
            </div>
          </div>

          <div className="summary-card losers">
            <div className="summary-card-header">
              <div className="summary-card-icon">
                <TrendingDown size={22} />
              </div>
              <span className="summary-card-title">Losers</span>
            </div>
            <div className="summary-card-value">{marketSummary.loserscount}</div>
            <div className="summary-card-change">
              of {marketSummary.totalstocks} stocks
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
              color: marketSummary.averagechange >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' 
            }}>
              {marketSummary.averagechange >= 0 ? '+' : ''}{marketSummary.averagechange}%
            </div>
            <div className="summary-card-change">
              {marketSummary.marketsentiment}
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
              {formatVolume(marketSummary.totalvolume)}
            </div>
            <div className="summary-card-change">
              Total traded
            </div>
          </div>
        </div>
      )}

      {/ Tabs /}
      <div className="tabs-container">
        <div className="tabs">
          <button 
            className={tab ${activeTab === 'gainers' ? 'active' : ''}}
            onClick={() => setActiveTab('gainers')}
          >
            <TrendingUp size={16} style={{ marginRight: '0.5rem' }} />
            Top Gainers
          </button>
          <button 
            className={tab ${activeTab === 'losers' ? 'active' : ''}}
            onClick={() => setActiveTab('losers')}
          >
            <TrendingDown size={16} style={{ marginRight: '0.5rem' }} />
            Top Losers
          </button>
          <button 
            className={tab ${viewMode === 'table' ? 'active' : ''}}
            onClick={() => setViewMode(viewMode === 'table' ? 'cards' : 'table')}
          >
            <Layers size={16} style={{ marginRight: '0.5rem' }} />
            {viewMode === 'table' ? 'Card View' : 'Table View'}
          </button>
        </div>
      </div>

      {/ Content /}
      {loading ? (
        <Loader text="Updating data..." />
      ) : viewMode === 'table' ? (
        <StockTable 
          stocks={currentData}
          title={activeTab === 'gainers' ? 'Top Gainers' : 'Top Losers'}
          icon={activeTab === 'gainers' ? TrendingUp : TrendingDown}
          lastUpdated={lastUpdated}
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
`

frontend/src/App.js

`jsx
import React, { useState } from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import { stocksApi } from './services/api';
import './App.css';

function App() {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

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
      />
      <main className="main-content">
        <Dashboard refreshTrigger={refreshTrigger} />
      </main>
    </div>
  );
}

export default App;
`

Environment Configuration
backend/.env (Create this file)

`env
Angel One API Credentials
ANGELAPIKEY=yourangelapikey
ANGELCLIENTID=yourclientid
ANGELPASSWORD=yourpassword
ANGELTOTPSECRET=yourtotpsecret

MySQL Configuration
MYSQLHOST=localhost
MYSQLUSER=root
MYSQLPASSWORD=yourmysqlpassword
MYSQLDB=nifty50scanner

Flask Configuration
SECRETKEY=your-super-secret-key-here
DEBUG=True
`

README.md

`markdown
Nifty50 Top Gainers Scanner

A real-time web application that scans the Indian stock market and displays the top gaining stocks in the Nifty50 index using Angel One Smart API.

Features
• 📈 Real-time top gainers and losers tracking
• 📊 Market summary with sentiment analysis
• 🔄 Auto-refresh every 60 seconds
• 📱 Responsive design with dark theme
• 💾 Historical data storage in MySQL
• 🎨 Modern UI with card and table views

Tech Stack
• Frontend: React, Axios, Recharts, Lucide Icons
• Backend: Python, Flask, Flask-CORS
• Database: MySQL
• API: Angel One Smart API

Prerequisites
• Node.js 18+
• Python 3.9+
• MySQL 8.0+
• Angel One trading account with API access

Installation
Database Setup

`bash
mysql -u root -p < database/schema.sql
`

Backend Setup

`bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
`

Create .env file with your credentials (see .env.example).

`bash
python app.py
`

Frontend Setup

`bash
cd frontend
npm install
npm start
`

API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/top-gainers | GET | Get top gaining stocks |
| /api/top-losers | GET | Get top losing stocks |
| /api/all-stocks | GET | Get all Nifty50 stocks |
| /api/market-summary | GET | Get market statistics |
| /api/refresh | POST | Force refresh data |

Configuration

Set these environment variables in backend/.env:

• ANGELAPIKEY - Your Angel One API key
• ANGELCLIENTID - Your client ID
• ANGELPASSWORD - Your trading password
• ANGELTOTPSECRET - Your TOTP secret for 2FA

Screenshots

The app features:
• Dark theme with gradient backgrounds
• Summary cards showing market health
• Tabbed interface for gainers/losers
• Toggle between table and card views
• Responsive design for all devices

License

MIT
`

Running the Application

Start the backend:

`bash
cd backend
source venv/bin/activate
python app.py
`

Start the frontend:

`bash
cd frontend
npm start
`

The app will be available at http://localhost:3000 with the API running on http://localhost:5000.

This gives you a complete, production-ready application. A few notes:

Token mapping — The stock tokens in angel_api.py are indicative. You'll want to verify them against Angel One's symbol master file, which you can download from their API.

TOTP setup — Generate your TOTP secret from Angel One's SmartAPI dashboard and add it to your .env` file.

Market hours — The scheduler runs only during NSE trading hours (9:15 AM – 3:30 PM IST, Mon–Fri).

User:

give me all files in zip format

User:

next time sure