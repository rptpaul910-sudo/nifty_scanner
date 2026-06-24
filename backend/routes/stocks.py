from flask import Blueprint, jsonify, request
from services.angel_api import AngelOneService, get_market_status

stocks_bp = Blueprint('stocks', __name__)

# In-memory cache — avoids hammering Yahoo Finance on every single request
_cache = {"data": [], "timestamp": None}
_service = AngelOneService()


def refresh_cache():
    """Fetch fresh data from Yahoo Finance and store in memory cache."""
    from datetime import datetime
    print("Refreshing stock data cache...")
    data = _service.get_all_nifty50_data()
    if data:
        _cache["data"] = data
        _cache["timestamp"] = datetime.now().isoformat()
        print(f"Cache refreshed: {len(data)} stocks at {_cache['timestamp']}")
    else:
        print("Cache refresh returned no data.")
    return data


def get_cached_or_fetch():
    """Return cached data if available, otherwise fetch fresh."""
    if not _cache["data"]:
        refresh_cache()
    return _cache["data"]


@stocks_bp.route('/api/top-gainers', methods=['GET'])
def get_top_gainers():
    try:
        limit = request.args.get('limit', 10, type=int)
        all_stocks = get_cached_or_fetch()
        gainers = sorted(all_stocks, key=lambda x: x['change_percent'], reverse=True)[:limit]
        return jsonify({
            "success": True,
            "data": gainers,
            "count": len(gainers),
            "cached_at": _cache["timestamp"],
            "market_status": get_market_status()
        })
    except Exception as e:
        print(f"top-gainers error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@stocks_bp.route('/api/top-losers', methods=['GET'])
def get_top_losers():
    try:
        limit = request.args.get('limit', 10, type=int)
        all_stocks = get_cached_or_fetch()
        losers = sorted(all_stocks, key=lambda x: x['change_percent'])[:limit]
        return jsonify({
            "success": True,
            "data": losers,
            "count": len(losers),
            "cached_at": _cache["timestamp"],
            "market_status": get_market_status()
        })
    except Exception as e:
        print(f"top-losers error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@stocks_bp.route('/api/all-stocks', methods=['GET'])
def get_all_stocks():
    try:
        stocks = get_cached_or_fetch()
        return jsonify({
            "success": True,
            "data": stocks,
            "count": len(stocks),
            "cached_at": _cache["timestamp"],
            "market_status": get_market_status()
        })
    except Exception as e:
        print(f"all-stocks error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@stocks_bp.route('/api/market-summary', methods=['GET'])
def get_market_summary():
    try:
        all_stocks = get_cached_or_fetch()
        if not all_stocks:
            return jsonify({"success": False, "error": "No data available"}), 500

        gainers   = [s for s in all_stocks if s['change_percent'] > 0]
        losers    = [s for s in all_stocks if s['change_percent'] < 0]
        unchanged = [s for s in all_stocks if s['change_percent'] == 0]
        avg_change = sum(s['change_percent'] for s in all_stocks) / len(all_stocks)

        return jsonify({
            "success": True,
            "data": {
                "total_stocks":     len(all_stocks),
                "gainers_count":    len(gainers),
                "losers_count":     len(losers),
                "unchanged_count":  len(unchanged),
                "total_volume":     sum(s['volume'] for s in all_stocks),
                "average_change":   round(avg_change, 2),
                "top_gainer":       max(all_stocks, key=lambda x: x['change_percent']),
                "top_loser":        min(all_stocks, key=lambda x: x['change_percent']),
                "market_sentiment": "Bullish" if len(gainers) > len(losers) else "Bearish"
            },
            "cached_at": _cache["timestamp"],
            "market_status": get_market_status()
        })
    except Exception as e:
        print(f"market-summary error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@stocks_bp.route('/api/refresh', methods=['POST'])
def force_refresh():
    try:
        data = refresh_cache()
        return jsonify({
            "success": bool(data),
            "message": f"Refreshed {len(data)} stocks" if data else "Refresh returned no data",
            "cached_at": _cache["timestamp"]
        })
    except Exception as e:
        print(f"refresh error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
