from flask import Blueprint, jsonify, request
from services.angel_api import AngelOneService, get_market_status
from services.database import mysql, save_stock_data, get_historical_gainers

stocks_bp = Blueprint('stocks', __name__)
angel_service = AngelOneService()

def ensure_logged_in():
    """Login if not already authenticated, or re-login if session expired."""
    if not angel_service.auth_token:
        print("No active session — logging in.")
        return angel_service.login()
    return True

def fetch_all_stocks():
    """
    Fetch all Nifty50 data. Works during AND after market hours since
    Angel One's getMarketData returns last-session values when market is closed.
    Re-attempts login once if the first fetch returns empty (handles expired sessions).
    """
    if not ensure_logged_in():
        print("Login failed — cannot fetch stock data.")
        return []

    data = angel_service.get_all_nifty50_data()

    if not data:
        # Session may have expired mid-run — try a fresh login and one more fetch.
        print("Empty data on first fetch — refreshing session and retrying.")
        angel_service.auth_token = None
        if angel_service.login():
            data = angel_service.get_all_nifty50_data()

    return data or []

@stocks_bp.route('/api/top-gainers', methods=['GET'])
def get_top_gainers():
    """Get top gaining stocks in Nifty50"""
    try:
        limit = request.args.get('limit', 10, type=int)
        all_stocks = fetch_all_stocks()
        all_stocks.sort(key=lambda x: x['change_percent'], reverse=True)
        gainers = all_stocks[:limit]

        if gainers:
            try:
                cursor = mysql.connection.cursor()
                for stock in gainers:
                    save_stock_data(cursor, stock)
                mysql.connection.commit()
                cursor.close()
            except Exception as db_error:
                print(f"Database error: {db_error}")

        return jsonify({
            "success": True,
            "data": gainers,
            "count": len(gainers),
            "market_status": get_market_status()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@stocks_bp.route('/api/all-stocks', methods=['GET'])
def get_all_stocks():
    """Get all Nifty50 stocks data"""
    try:
        stocks = fetch_all_stocks()
        return jsonify({
            "success": True,
            "data": stocks,
            "count": len(stocks),
            "market_status": get_market_status()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@stocks_bp.route('/api/top-losers', methods=['GET'])
def get_top_losers():
    """Get top losing stocks in Nifty50"""
    try:
        limit = request.args.get('limit', 10, type=int)
        all_stocks = fetch_all_stocks()
        all_stocks.sort(key=lambda x: x['change_percent'])
        losers = all_stocks[:limit]
        return jsonify({
            "success": True,
            "data": losers,
            "count": len(losers),
            "market_status": get_market_status()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@stocks_bp.route('/api/market-summary', methods=['GET'])
def get_market_summary():
    """Get market summary statistics"""
    try:
        all_stocks = fetch_all_stocks()

        if not all_stocks:
            return jsonify({"success": False, "error": "No data available"}), 500

        gainers   = [s for s in all_stocks if s['change_percent'] > 0]
        losers    = [s for s in all_stocks if s['change_percent'] < 0]
        unchanged = [s for s in all_stocks if s['change_percent'] == 0]

        total_volume = sum(s['volume'] for s in all_stocks)
        avg_change   = sum(s['change_percent'] for s in all_stocks) / len(all_stocks)
        top_gainer   = max(all_stocks, key=lambda x: x['change_percent'])
        top_loser    = min(all_stocks, key=lambda x: x['change_percent'])

        return jsonify({
            "success": True,
            "data": {
                "total_stocks":     len(all_stocks),
                "gainers_count":    len(gainers),
                "losers_count":     len(losers),
                "unchanged_count":  len(unchanged),
                "total_volume":     total_volume,
                "average_change":   round(avg_change, 2),
                "top_gainer":       top_gainer,
                "top_loser":        top_loser,
                "market_sentiment": "Bullish" if len(gainers) > len(losers) else "Bearish"
            },
            "market_status": get_market_status()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@stocks_bp.route('/api/historical-gainers', methods=['GET'])
def get_historical():
    """Get historical top gainers"""
    try:
        limit = request.args.get('limit', 10, type=int)
        days = request.args.get('days', 7, type=int)
        
        cursor = mysql.connection.cursor()
        historical = get_historical_gainers(cursor, limit, days)
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

@stocks_bp.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Force refresh — clears session so next fetch re-authenticates."""
    try:
        angel_service.auth_token = None   # force re-login on next call
        data = fetch_all_stocks()
        if data:
            return jsonify({
                "success": True,
                "message": "Data refreshed successfully",
                "count": len(data)
            })
        return jsonify({"success": False, "error": "Login or data fetch failed after refresh"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
