import yfinance as yf
from datetime import datetime, time as dtime
import pytz

IST = pytz.timezone("Asia/Kolkata")


def get_market_status():
    now = datetime.now(IST)
    is_weekday   = now.weekday() < 5
    market_open  = dtime(9, 15)
    market_close = dtime(15, 30)
    is_open = is_weekday and market_open <= now.time() <= market_close
    return {
        "is_open":    is_open,
        "label":      "Market Open" if is_open else "Market Closed",
        "note":       None if is_open else "Showing last session data (market is closed).",
        "checked_at": now.isoformat()
    }


class AngelOneService:
    """
    Data provider using Yahoo Finance (yfinance).
    No API key, no login, no session tokens required.
    Works 24/7 — during market hours returns live/delayed data,
    outside hours returns last session close data.
    Yahoo Finance tickers for NSE stocks use the '.NS' suffix.
    """

    def __init__(self):
        # No credentials needed
        self.auth_token = None   # kept for compatibility with routes.py

        self.nifty50_stocks = [
            {"symbol": "RELIANCE",   "ticker": "RELIANCE.NS",   "name": "Reliance Industries"},
            {"symbol": "TCS",        "ticker": "TCS.NS",        "name": "Tata Consultancy Services"},
            {"symbol": "HDFCBANK",   "ticker": "HDFCBANK.NS",   "name": "HDFC Bank"},
            {"symbol": "INFY",       "ticker": "INFY.NS",       "name": "Infosys"},
            {"symbol": "ICICIBANK",  "ticker": "ICICIBANK.NS",  "name": "ICICI Bank"},
            {"symbol": "HINDUNILVR", "ticker": "HINDUNILVR.NS", "name": "Hindustan Unilever"},
            {"symbol": "SBIN",       "ticker": "SBIN.NS",       "name": "State Bank of India"},
            {"symbol": "BHARTIARTL", "ticker": "BHARTIARTL.NS", "name": "Bharti Airtel"},
            {"symbol": "ITC",        "ticker": "ITC.NS",        "name": "ITC"},
            {"symbol": "KOTAKBANK",  "ticker": "KOTAKBANK.NS",  "name": "Kotak Mahindra Bank"},
            {"symbol": "LT",         "ticker": "LT.NS",         "name": "Larsen & Toubro"},
            {"symbol": "AXISBANK",   "ticker": "AXISBANK.NS",   "name": "Axis Bank"},
            {"symbol": "ASIANPAINT", "ticker": "ASIANPAINT.NS", "name": "Asian Paints"},
            {"symbol": "MARUTI",     "ticker": "MARUTI.NS",     "name": "Maruti Suzuki"},
            {"symbol": "SUNPHARMA",  "ticker": "SUNPHARMA.NS",  "name": "Sun Pharmaceutical"},
            {"symbol": "TITAN",      "ticker": "TITAN.NS",      "name": "Titan Company"},
            {"symbol": "BAJFINANCE", "ticker": "BAJFINANCE.NS", "name": "Bajaj Finance"},
            {"symbol": "WIPRO",      "ticker": "WIPRO.NS",      "name": "Wipro"},
            {"symbol": "ULTRACEMCO", "ticker": "ULTRACEMCO.NS", "name": "UltraTech Cement"},
            {"symbol": "NESTLEIND",  "ticker": "NESTLEIND.NS",  "name": "Nestle India"},
            {"symbol": "POWERGRID",  "ticker": "POWERGRID.NS",  "name": "Power Grid Corporation"},
            {"symbol": "NTPC",       "ticker": "NTPC.NS",       "name": "NTPC"},
            {"symbol": "TECHM",      "ticker": "TECHM.NS",      "name": "Tech Mahindra"},
            {"symbol": "HCLTECH",    "ticker": "HCLTECH.NS",    "name": "HCL Technologies"},
            {"symbol": "ONGC",       "ticker": "ONGC.NS",       "name": "ONGC"},
            {"symbol": "TATAMOTORS", "ticker": "TATAMOTORS.NS", "name": "Tata Motors"},
            {"symbol": "TATASTEEL",  "ticker": "TATASTEEL.NS",  "name": "Tata Steel"},
            {"symbol": "ADANIENT",   "ticker": "ADANIENT.NS",   "name": "Adani Enterprises"},
            {"symbol": "ADANIPORTS", "ticker": "ADANIPORTS.NS", "name": "Adani Ports"},
            {"symbol": "COALINDIA",  "ticker": "COALINDIA.NS",  "name": "Coal India"},
            {"symbol": "DIVISLAB",   "ticker": "DIVISLAB.NS",   "name": "Divi's Laboratories"},
            {"symbol": "DRREDDY",    "ticker": "DRREDDY.NS",    "name": "Dr. Reddy's Laboratories"},
            {"symbol": "EICHERMOT",  "ticker": "EICHERMOT.NS",  "name": "Eicher Motors"},
            {"symbol": "GRASIM",     "ticker": "GRASIM.NS",     "name": "Grasim Industries"},
            {"symbol": "HDFCLIFE",   "ticker": "HDFCLIFE.NS",   "name": "HDFC Life"},
            {"symbol": "HEROMOTOCO", "ticker": "HEROMOTOCO.NS", "name": "Hero MotoCorp"},
            {"symbol": "HINDALCO",   "ticker": "HINDALCO.NS",   "name": "Hindalco Industries"},
            {"symbol": "INDUSINDBK", "ticker": "INDUSINDBK.NS", "name": "IndusInd Bank"},
            {"symbol": "JSWSTEEL",   "ticker": "JSWSTEEL.NS",   "name": "JSW Steel"},
            {"symbol": "M&M",        "ticker": "M&M.NS",        "name": "Mahindra & Mahindra"},
            {"symbol": "CIPLA",      "ticker": "CIPLA.NS",      "name": "Cipla"},
            {"symbol": "BAJAJFINSV", "ticker": "BAJAJFINSV.NS", "name": "Bajaj Finserv"},
            {"symbol": "BAJAJ-AUTO", "ticker": "BAJAJ-AUTO.NS", "name": "Bajaj Auto"},
            {"symbol": "APOLLOHOSP", "ticker": "APOLLOHOSP.NS", "name": "Apollo Hospitals"},
            {"symbol": "BRITANNIA",  "ticker": "BRITANNIA.NS",  "name": "Britannia Industries"},
            {"symbol": "SBILIFE",    "ticker": "SBILIFE.NS",    "name": "SBI Life Insurance"},
            {"symbol": "TATACONSUM", "ticker": "TATACONSUM.NS", "name": "Tata Consumer Products"},
            {"symbol": "UPL",        "ticker": "UPL.NS",        "name": "UPL"},
            {"symbol": "BPCL",       "ticker": "BPCL.NS",       "name": "Bharat Petroleum"},
            {"symbol": "SHREECEM",   "ticker": "SHREECEM.NS",   "name": "Shree Cement"},
        ]

    def login(self):
        """No-op: yfinance needs no authentication."""
        print("Yahoo Finance provider — no login required.")
        self.auth_token = "yfinance"   # truthy value so routes.py checks pass
        return True

    def get_all_nifty50_data(self):
        """
        Fetch all 50 Nifty stocks in a single yfinance batch call.
        Returns live/delayed data during market hours,
        last-session close data when market is closed.
        """
        tickers = [s["ticker"] for s in self.nifty50_stocks]
        ticker_to_meta = {s["ticker"]: s for s in self.nifty50_stocks}

        print(f"Fetching {len(tickers)} Nifty50 tickers via Yahoo Finance...")

        try:
            # Single batch download — much faster than 50 individual calls
            data = yf.download(
                tickers,
                period="2d",        # 2 days so we always have a previous close
                interval="1d",
                group_by="ticker",
                auto_adjust=True,
                progress=False,
                threads=True
            )
        except Exception as e:
            print(f"yfinance batch download error: {e}")
            return []

        results = []
        for stock in self.nifty50_stocks:
            try:
                ticker = stock["ticker"]

                # Extract this ticker's rows from the multi-ticker dataframe
                if len(tickers) > 1:
                    df = data[ticker].dropna(how="all")
                else:
                    df = data.dropna(how="all")

                if df.empty or len(df) < 1:
                    print(f"No data for {ticker}")
                    continue

                latest   = df.iloc[-1]
                prev     = df.iloc[-2] if len(df) >= 2 else latest

                close    = float(latest["Close"])
                open_    = float(latest["Open"])
                high     = float(latest["High"])
                low      = float(latest["Low"])
                volume   = int(latest["Volume"])
                prev_close = float(prev["Close"])

                change   = round(close - prev_close, 2)
                change_pct = round((change / prev_close * 100) if prev_close else 0, 2)

                results.append({
                    "symbol":         stock["symbol"],
                    "name":           stock["name"],
                    "token":          ticker,
                    "ltp":            round(close, 2),
                    "open":           round(open_, 2),
                    "high":           round(high, 2),
                    "low":            round(low, 2),
                    "close":          round(close, 2),
                    "change":         change,
                    "change_percent": change_pct,
                    "volume":         volume
                })

            except Exception as e:
                print(f"Error processing {stock['symbol']}: {e}")
                continue

        print(f"Successfully fetched {len(results)}/50 stocks.")
        return results

    def scan_top_gainers(self, limit=10):
        data = self.get_all_nifty50_data()
        data.sort(key=lambda x: x["change_percent"], reverse=True)
        return data[:limit]

    def logout(self):
        """No-op: yfinance needs no session termination."""
        return True
