from SmartApi import SmartConnect
import pyotp
from config import Config
from datetime import datetime, time as dtime


def get_market_status():
    """
    Determine if NSE is currently open.
    NSE regular session: Mon-Fri, 09:15 - 15:30 IST.
    Note: Does not account for exchange holidays.
    """
    now = datetime.now()
    is_weekday = now.weekday() < 5  # Mon=0 ... Fri=4
    market_open  = dtime(9, 15)
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
        self.api_key      = Config.ANGEL_API_KEY
        self.client_id    = Config.ANGEL_CLIENT_ID
        self.password     = Config.ANGEL_PASSWORD
        self.totp_secret  = Config.ANGEL_TOTP_SECRET
        self.smart_api    = None
        self.auth_token   = None
        self.refresh_token = None
        self.feed_token   = None

        # Nifty 50 stock tokens (NSE) — 50 unique entries
        self.nifty50_stocks = [
            {"symbol": "RELIANCE",    "token": "2885",  "name": "Reliance Industries"},
            {"symbol": "TCS",         "token": "11536", "name": "Tata Consultancy Services"},
            {"symbol": "HDFCBANK",    "token": "1333",  "name": "HDFC Bank"},
            {"symbol": "INFY",        "token": "1594",  "name": "Infosys"},
            {"symbol": "ICICIBANK",   "token": "4963",  "name": "ICICI Bank"},
            {"symbol": "HINDUNILVR",  "token": "1394",  "name": "Hindustan Unilever"},
            {"symbol": "SBIN",        "token": "3045",  "name": "State Bank of India"},
            {"symbol": "BHARTIARTL",  "token": "10604", "name": "Bharti Airtel"},
            {"symbol": "ITC",         "token": "1660",  "name": "ITC"},
            {"symbol": "KOTAKBANK",   "token": "1922",  "name": "Kotak Mahindra Bank"},
            {"symbol": "LT",          "token": "11483", "name": "Larsen & Toubro"},
            {"symbol": "AXISBANK",    "token": "5900",  "name": "Axis Bank"},
            {"symbol": "ASIANPAINT",  "token": "236",   "name": "Asian Paints"},
            {"symbol": "MARUTI",      "token": "10999", "name": "Maruti Suzuki"},
            {"symbol": "SUNPHARMA",   "token": "3351",  "name": "Sun Pharmaceutical"},
            {"symbol": "TITAN",       "token": "3506",  "name": "Titan Company"},
            {"symbol": "BAJFINANCE",  "token": "317",   "name": "Bajaj Finance"},
            {"symbol": "WIPRO",       "token": "3787",  "name": "Wipro"},
            {"symbol": "ULTRACEMCO",  "token": "11532", "name": "UltraTech Cement"},
            {"symbol": "NESTLEIND",   "token": "17963", "name": "Nestle India"},
            {"symbol": "POWERGRID",   "token": "14977", "name": "Power Grid Corporation"},
            {"symbol": "NTPC",        "token": "11630", "name": "NTPC"},
            {"symbol": "TECHM",       "token": "13538", "name": "Tech Mahindra"},
            {"symbol": "HCLTECH",     "token": "7229",  "name": "HCL Technologies"},
            {"symbol": "ONGC",        "token": "2475",  "name": "Oil & Natural Gas Corporation"},
            {"symbol": "TATAMOTORS",  "token": "3456",  "name": "Tata Motors"},
            {"symbol": "TATASTEEL",   "token": "3499",  "name": "Tata Steel"},
            {"symbol": "ADANIENT",    "token": "25",    "name": "Adani Enterprises"},
            {"symbol": "ADANIPORTS",  "token": "15083", "name": "Adani Ports"},
            {"symbol": "COALINDIA",   "token": "20374", "name": "Coal India"},
            {"symbol": "DIVISLAB",    "token": "10940", "name": "Divi's Laboratories"},
            {"symbol": "DRREDDY",     "token": "881",   "name": "Dr. Reddy's Laboratories"},
            {"symbol": "EICHERMOT",   "token": "910",   "name": "Eicher Motors"},
            {"symbol": "GRASIM",      "token": "1232",  "name": "Grasim Industries"},
            {"symbol": "HDFCLIFE",    "token": "467",   "name": "HDFC Life"},
            {"symbol": "HEROMOTOCO",  "token": "1348",  "name": "Hero MotoCorp"},
            {"symbol": "HINDALCO",    "token": "1363",  "name": "Hindalco Industries"},
            {"symbol": "INDUSINDBK",  "token": "5258",  "name": "IndusInd Bank"},
            {"symbol": "JSWSTEEL",    "token": "11723", "name": "JSW Steel"},
            {"symbol": "M&M",         "token": "2031",  "name": "Mahindra & Mahindra"},
            {"symbol": "CIPLA",       "token": "694",   "name": "Cipla"},
            {"symbol": "BAJAJFINSV",  "token": "16675", "name": "Bajaj Finserv"},
            {"symbol": "BAJAJ-AUTO",  "token": "16669", "name": "Bajaj Auto"},
            {"symbol": "APOLLOHOSP",  "token": "157",   "name": "Apollo Hospitals"},
            {"symbol": "BRITANNIA",   "token": "547",   "name": "Britannia Industries"},
            {"symbol": "SBILIFE",     "token": "21808", "name": "SBI Life Insurance"},
            {"symbol": "TATACONSUM",  "token": "3432",  "name": "Tata Consumer Products"},
            {"symbol": "UPL",         "token": "11287", "name": "UPL"},
            {"symbol": "BPCL",        "token": "526",   "name": "Bharat Petroleum"},
            {"symbol": "SHREECEM",    "token": "3103",  "name": "Shree Cement"},
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

            if data and data.get('status'):
                self.auth_token   = data['data']['jwtToken']
                self.refresh_token = data['data']['refreshToken']
                self.feed_token   = self.smart_api.getfeedToken()
                print("Angel One login succeeded.")
                return True

            # API responded without raising, but rejected the login —
            # wrong credentials, TOTP mismatch, IP not whitelisted, etc.
            print(f"Angel One login REJECTED. Full response: {data}")
            return False

        except Exception as e:
            print(f"Login error (exception): {e}")
            return False

    def _fetch_stock(self, stock):
        """Fetch FULL quote for a single stock token. Returns dict or None."""
        try:
            response = self.smart_api.getMarketData({
                "mode": "FULL",
                "exchangeTokens": {"NSE": [stock["token"]]}
            })

            if response and response.get('status') and response.get('data'):
                fetched = response['data'].get('fetched', [])
                if fetched:
                    d = fetched[0]
                    ltp   = float(d.get('ltp', 0))
                    close = float(d.get('close', 0))
                    change         = ltp - close if close > 0 else 0
                    change_percent = ((ltp - close) / close * 100) if close > 0 else 0

                    return {
                        "symbol":         stock["symbol"],
                        "name":           stock["name"],
                        "token":          stock["token"],
                        "ltp":            round(ltp, 2),
                        "open":           round(float(d.get('open', 0)), 2),
                        "high":           round(float(d.get('high', 0)), 2),
                        "low":            round(float(d.get('low', 0)), 2),
                        "close":          round(close, 2),
                        "change":         round(change, 2),
                        "change_percent": round(change_percent, 2),
                        "volume":         int(d.get('tradeVolume', 0))
                    }
            return None

        except Exception as e:
            print(f"Error fetching {stock['symbol']}: {e}")
            return None

    def get_all_nifty50_data(self):
        """
        Fetch all 50 Nifty stocks. Works during market hours (live LTP)
        and after hours (last session close). Returns [] only if login fails.
        """
        stocks_data = []
        first_failure_logged = False

        for stock in self.nifty50_stocks:
            result = self._fetch_stock(stock)
            if result:
                stocks_data.append(result)
            elif not first_failure_logged:
                print(f"getMarketData returned no data for {stock['symbol']} "
                      f"(auth_token present: {bool(self.auth_token)})")
                first_failure_logged = True

        print(f"get_all_nifty50_data: fetched {len(stocks_data)}/50 stocks.")
        return stocks_data

    def scan_top_gainers(self, limit=10):
        """Return top N gainers from Nifty50, sorted by change_percent desc."""
        data = self.get_all_nifty50_data()
        data.sort(key=lambda x: x['change_percent'], reverse=True)
        return data[:limit]

    def logout(self):
        """Logout from Angel One API"""
        try:
            if self.smart_api:
                self.smart_api.terminateSession(self.client_id)
                return True
        except Exception as e:
            print(f"Logout error: {e}")
        return False
