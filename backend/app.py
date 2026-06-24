import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.stocks import stocks_bp
from apscheduler.schedulers.background import BackgroundScheduler
from services.angel_api import AngelOneService

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(stocks_bp)

# Background scheduler — refreshes cache every 5 min during market hours
def scheduled_scan():
    with app.app_context():
        try:
            from routes.stocks import refresh_cache
            refresh_cache()
            print("Scheduled scan completed.")
        except Exception as e:
            print(f"Scheduled scan error: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(
    scheduled_scan,
    'cron',
    day_of_week='mon-fri',
    hour='9-15',
    minute='*/5'
)

@app.route('/')
def home():
    return jsonify({
        "message": "Nifty50 Scanner API (Yahoo Finance)",
        "version": "2.0.0",
        "endpoints": {
            "top_gainers":    "/api/top-gainers",
            "top_losers":     "/api/top-losers",
            "all_stocks":     "/api/all-stocks",
            "market_summary": "/api/market-summary",
            "refresh":        "/api/refresh"
        }
    })

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    scheduler.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
