from SmartApi import SmartConnect
import pyotp
from config import Config
from datetime import datetime, time as dtime, timedelta
import pytz


IST = pytz.timezone("Asia/Kolkata")


def get_market_status():
    now = datetime.now(IST)
    is_weekday   = now.weekday() < 5
    market_open  = dtime(9, 15)
    market_close = dtime(15, 30)
    is_open = is_weekday and market_open <= now.time() <= market_close
    return {
        "is_open":   is_open,
        "label":     "Market Open" if is_open else "Market Closed",
        "note":      None if is_open else "Showing last session data (market is closed).",
        "checked_at": now.isoformat()
    }


def last_trading_day():
    """Return the most recent weekday (Mon-Fri) as a date object (IST)."""
    today = datetime.now(IST).date()
    d = today
    while d.weekday() >= 5:   # Sat=5, Sun=6
        d -= timedelta(days=1)
    return d


class AngelOneService:
    def __init__(self):
        self.api_key       = Config.ANGEL_API_KEY
        self.client_id     = Config.ANGEL_CLIENT_ID
        self.password      = Config.ANGEL_PASSWORD
        self.totp_secret   = Config.ANGEL_TOTP_SECRET
        self.smart_api     = None
        self.auth_token    = None
        self.refresh_token = None
        self.feed_token    = None

        self.nifty50_stocks = [
            {"symbol": "RELIANCE",   "token": "2885",  "name": "Reliance Industries"},
            {"symbol": "TCS",        "token": "11536", "name": "Tata Consultancy Services"},
            {"symbol": "HDFCBANK",   "token": "1333",  "name": "HDFC Bank"},
            {"symbol": "INFY",       "token": "1594",  "name": "Infosys"},
            {"symbol": "ICICIBANK",  "token": "4963",  "name": "ICICI Bank"},
            {"symbol": "HINDUNILVR", "token": "1394",  "name": "Hindustan Unilever"},
            {"symbol": "SBIN",       "token": "3045",  "name": "State Bank of India"},
            {"symbol": "BHARTIARTL","token": "10604",  "name": "Bharti Airtel"},
            {"symbol": "ITC",        "token": "1660",  "name": "ITC"},
            {"symbol": "KOTAKBANK",  "token": "1922",  "name": "Kotak Mahindra Bank"},
            {"symbol": "LT",         "token": "11483", "name": "Larsen & Toubro"},
            {"symbol": "AXISBANK",   "token": "5900",  "name": "Axis Bank"},
            {"symbol": "ASIANPAINT", "token": "236",   "name": "Asian Paints"},
            {"symbol": "MARUTI",     "token": "10999", "name": "Maruti Suzuki"},
            {"symbol": "SUNPHARMA",  "token": "3351",  "name": "Sun Pharmaceutical"},
            {"symbol": "TITAN",      "token": "3506",  "name": "Titan Company"},
            {"symbol": "BAJFINANCE", "token": "317",   "name": "Bajaj Finance"},
            {"symbol": "WIPRO",      "token": "3787",  "name": "Wipro"},
            {"symbol": "ULTRACEMCO", "token": "11532", "name": "UltraTech Cement"},
            {"symbol": "NESTLEIND",  "token": "17963", "name": "Nestle India"},
            {"symbol": "POWERGRID",  "token": "14977", "name": "Power Grid Corporation"},
            {"symbol": "NTPC",       "token": "11630", "name": "NTPC"},
            {"symbol": "TECHM",      "token": "13538", "name": "Tech Mahindra"},
            {"symbol": "HCLTECH",    "token": "7229",  "name": "HCL Technologies"},
            {"symbol": "ONGC",       "token": "2475",  "name": "ONGC"},
            {"symbol": "TATAMOTORS", "token": "3456",  "name": "Tata Motors"},
            {"symbol": "TATASTEEL",  "token": "3499",  "name": "Tata Steel"},
            {"symbol": "ADANIENT",   "token": "25",    "name": "Adani Enterprises"},
            {"symbol": "ADANIPORTS", "token": "15083", "name": "Adani Ports"},
            {"symbol": "COALINDIA",  "token": "20374", "name": "Coal India"},
            {"symbol": "DIVISLAB",   "token": "10940", "name": "Divi's Laboratories"},
            {"symbol": "DRREDDY",    "token": "881",   "name": "Dr. Reddy's Laboratories"},
            {"symbol": "EICHERMOT",  "token": "910",   "name": "Eicher Motors"},
            {"symbol": "GRASIM",     "token": "1232",  "name": "Grasim Industries"},
            {"symbol": "HDFCLIFE",   "token": "467",   "name": "HDFC Life"},
            {"symbol": "HEROMOTOCO", "token": "1348",  "name": "Hero MotoCorp"},
            {"symbol": "HINDALCO",   "token": "1363",  "name": "Hindalco Industries"},
            {"symbol": "INDUSINDBK", "token": "5258",  "name": "IndusInd Bank"},
            {"symbol": "JSWSTEEL",   "token": "11723", "name": "JSW Steel"},
            {"symbol": "M&M",        "token": "2031",  "name": "Mahindra & Mahindra"},
            {"symbol": "CIPLA",      "token": "694",   "name": "Cipla"},
            {"symbol": "BAJAJFINSV", "token": "16675", "name": "Bajaj Finserv"},
            {"symbol": "BAJAJ-AUTO", "token": "16669", "name": "Bajaj Auto"},
            {"symbol": "APOLLOHOSP", "token": "157",   "name": "Apollo Hospitals"},
            {"symbol": "BRITANNIA",  "token": "547",   "name": "Britannia Industries"},
            {"symbol": "SBILIFE",    "token": "21808", "name": "SBI Life Insurance"},
            {"symbol": "TATACONSUM", "token": "3432",  "name": "Tata Consumer Products"},
            {"symbol": "UPL",        "token": "11287", "name": "UPL"},
            {"symbol": "BPCL",       "token": "526",   "name": "Bharat Petroleum"},
            {"symbol": "SHREECEM",   "token": "3103",  "name": "Shree Cement"},
        ]

    # ------------------------------------------------------------------
    def login(self):
        try:
            self.smart_api = SmartConnect(api_key=self.api_key)
            totp = pyotp.TOTP(self.totp_secret).now()
            data = self.smart_api.generateSession(
                clientCode=self.client_id,
                password=self.password,
                totp=totp
            )
            if data and data.get('status'):
                self.auth_token    = data['data']['jwtToken']
                self.refresh_token = data['data']['refreshToken']
                self.feed_token    = self.smart_api.getfeedToken()
                print("Angel One login succeeded.")
                return True
            print(f"Angel One login REJECTED. Full response: {data}")
            return False
        except Exception as e:
            print(f"Login error (exception): {e}")
            return False

    # ------------------------------------------------------------------
    def _fetch_live(self, stock):
        """Fetch via getMarketData — works only during market hours."""
        try:
            response = self.smart_api.getMarketData({
                "mode": "FULL",
                "exchangeTokens": {"NSE": [stock["token"]]}
            })
            if response and response.get('status') and response.get('data'):
                fetched = response['data'].get('fetched', [])
                if fetched:
                    d      = fetched[0]
                    ltp    = float(d.get('ltp', 0))
                    close  = float(d.get('close', 0))
                    change = ltp - close if close > 0 else 0
                    pct    = (change / close * 100) if close > 0 else 0
                    return {
                        "symbol": stock["symbol"], "name": stock["name"],
                        "token":  stock["token"],
                        "ltp": round(ltp, 2),
                        "open":  round(float(d.get('open', 0)), 2),
                        "high":  round(float(d.get('high', 0)), 2),
                        "low":   round(float(d.get('low', 0)), 2),
                        "close": round(close, 2),
                        "change": round(change, 2),
                        "change_percent": round(pct, 2),
                        "volume": int(d.get('tradeVolume', 0))
                    }
        except Exception as e:
            print(f"Live fetch error {stock['symbol']}: {e}")
        return None

    def _fetch_historical(self, stock):
        """
        Fetch last trading session's OHLC via getCandleData.
        Used when market is closed — always returns last-session data.
        """
        try:
            day = last_trading_day()
            from_dt = f"{day} 09:15"
            to_dt   = f"{day} 15:30"
            params = {
                "exchange":    "NSE",
                "symboltoken": stock["token"],
                "interval":    "ONE_DAY",
                "fromdate":    from_dt,
                "todate":      to_dt
            }
            resp = self.smart_api.getCandleData(params)
            if resp and resp.get('status') and resp.get('data'):
                candles = resp['data']
                if candles:
                    # ONE_DAY candle: [timestamp, open, high, low, close, volume]
                    c     = candles[-1]
                    open_ = float(c[1])
                    high  = float(c[2])
                    low   = float(c[3])
                    close = float(c[4])
                    vol   = int(c[5])
                    # For closed-market, ltp = close; prev close unavailable here
                    # so change shows 0 (last session's own change is unknown
                    # without an additional prev-day candle fetch).
                    return {
                        "symbol": stock["symbol"], "name": stock["name"],
                        "token":  stock["token"],
                        "ltp":   round(close, 2),
                        "open":  round(open_, 2),
                        "high":  round(high, 2),
                        "low":   round(low, 2),
                        "close": round(close, 2),
                        "change": 0.0,
                        "change_percent": 0.0,
                        "volume": vol
                    }
            print(f"Historical fetch empty for {stock['symbol']}. Response: {resp}")
        except Exception as e:
            print(f"Historical fetch error {stock['symbol']}: {e}")
        return None

    # ------------------------------------------------------------------
    def get_all_nifty50_data(self):
        """
        Primary data fetch method.
        - During market hours: uses live getMarketData (LTP, real-time change%).
        - When market is closed: uses getCandleData (last session OHLC).
        Always returns data — never empty due to market being closed.
        """
        status   = get_market_status()
        use_live = status["is_open"]
        mode     = "LIVE" if use_live else "HISTORICAL"
        print(f"Fetching Nifty50 data in {mode} mode (market {'open' if use_live else 'closed'}).")

        results = []
        first_failure_logged = False

        for stock in self.nifty50_stocks:
            data = self._fetch_live(stock) if use_live else self._fetch_historical(stock)
            if data:
                results.append(data)
            elif not first_failure_logged:
                print(f"No data returned for {stock['symbol']} in {mode} mode.")
                first_failure_logged = True

        print(f"Fetched {len(results)}/50 stocks.")
        return results

    def scan_top_gainers(self, limit=10):
        data = self.get_all_nifty50_data()
        data.sort(key=lambda x: x['change_percent'], reverse=True)
        return data[:limit]

    def logout(self):
        try:
            if self.smart_api:
                self.smart_api.terminateSession(self.client_id)
                return True
        except Exception as e:
            print(f"Logout error: {e}")
        return False
