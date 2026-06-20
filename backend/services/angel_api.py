from SmartApi import SmartConnect
import pyotp
from config import Config
from datetime import datetime, time as dtime
import json
import requests


def get_market_status():
    """
    Determine if NSE is currently open.
    NSE regular session: Mon-Fri, 09:15 - 15:30 IST.
    Does not account for exchange holidays (would need a holiday calendar feed).
    """
    now = datetime.now()
    is_weekday = now.weekday() < 5  # Mon=0 ... Fri=4
    market_open = dtime(9, 15)
    market_close = dtime(15, 30)
    is_open = is_weekday and market_open <= now.time() <= market_close

    return {
        "is_open": is_open,
        "label": "Market Open" if is_open else "Market Closed",
        "note": None if is_open else "Showing last available traded data (LTP/close from the last session).",
        "checked_at": now.isoformat()
    }


class AngelOneService:
    def __init__(self):
        self.api_key = Config.ANGEL_API_KEY
        self.client_id = Config.ANGEL_CLIENT_ID
        self.password = Config.ANGEL_PASSWORD
        self.totp_secret = Config.ANGEL_TOTP_SECRET
        self.smart_api = None
        self.auth_token = None
        self.refresh_token = None
        self.feed_token = None
        
        # Nifty 50 stock tokens (NSE)
        self.nifty50_stocks = [
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
            self.smart_api = SmartConnect(api_key=self.api_key)
            totp = pyotp.TOTP(self.totp_secret).now()
            
            data = self.smart_api.generateSession(
                clientCode=self.client_id,
                password=self.password,
                totp=totp
            )
            
            if data['status']:
                self.auth_token = data['data']['jwtToken']
                self.refresh_token = data['data']['refreshToken']
                self.feed_token = self.smart_api.getfeedToken()
                return True
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def get_ltp_data(self, symbol_token, exchange="NSE"):
        """Get Last Traded Price data for a stock"""
        try:
            ltp_data = self.smart_api.ltpData(exchange, symbol_token, symbol_token)
            return ltp_data
        except Exception as e:
            print(f"LTP Error for {symbol_token}: {e}")
            return None
    
    def get_quote(self, symbol_token, exchange="NSE"):
        """Get detailed quote for a stock"""
        try:
            quote_params = {
                "mode": "FULL",
                "exchangeTokens": {
                    exchange: [symbol_token]
                }
            }
            quote_data = self.smart_api.getMarketData(quote_params)
            return quote_data
        except Exception as e:
            print(f"Quote Error for {symbol_token}: {e}")
            return None
    
    def scan_top_gainers(self, limit=10):
        """Scan all Nifty50 stocks and return top gainers"""
        if not self.smart_api:
            if not self.login():
                return []
        
        stocks_data = []
        
        for stock in self.nifty50_stocks:
            try:
                quote_params = {
                    "mode": "FULL",
                    "exchangeTokens": {
                        "NSE": [stock["token"]]
                    }
                }
                
                response = self.smart_api.getMarketData(quote_params)
                
                if response and response.get('status') and response.get('data'):
                    fetched = response['data']['fetched']
                    if fetched:
                        data = fetched[0]
                        ltp = float(data.get('ltp', 0))
                        close = float(data.get('close', 0))
                        open_price = float(data.get('open', 0))
                        high = float(data.get('high', 0))
                        low = float(data.get('low', 0))
                        volume = int(data.get('tradeVolume', 0))
                        
                        if close > 0:
                            change = ltp - close
                            change_percent = ((ltp - close) / close) * 100
                        else:
                            change = 0
                            change_percent = 0
                        
                        stocks_data.append({
                            "symbol": stock["symbol"],
                            "name": stock["name"],
                            "token": stock["token"],
                            "ltp": round(ltp, 2),
                            "open": round(open_price, 2),
                            "high": round(high, 2),
                            "low": round(low, 2),
                            "close": round(close, 2),
                            "change": round(change, 2),
                            "change_percent": round(change_percent, 2),
                            "volume": volume
                        })
                        
            except Exception as e:
                print(f"Error fetching {stock['symbol']}: {e}")
                continue
        
        # Sort by change_percent descending (top gainers)
        stocks_data.sort(key=lambda x: x['change_percent'], reverse=True)
        
        return stocks_data[:limit]
    
    def get_all_nifty50_data(self):
        """Get data for all Nifty50 stocks"""
        return self.scan_top_gainers(limit=50)
    
    def logout(self):
        """Logout from Angel One API"""
        try:
            if self.smart_api:
                self.smart_api.terminateSession(self.client_id)
                return True
        except Exception as e:
            print(f"Logout error: {e}")
        return False
