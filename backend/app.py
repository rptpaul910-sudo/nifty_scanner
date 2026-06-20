from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from services.database import init_db
from routes.stocks import stocks_bp
from apscheduler.schedulers.background import BackgroundScheduler
from services.angel_api import AngelOneService

app = Flask(__name__)
app.config.from_object(Config)

# MySQL Configuration
app.config['MYSQL_HOST'] = Config.MYSQL_HOST
app.config['MYSQL_USER'] = Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Config.MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize extensions
CORS(app, resources={r"/api/*": {"origins": "*"}})
mysql = init_db(app)

# Register blueprints
app.register_blueprint(stocks_bp)

# Background scheduler for periodic data refresh
def scheduled_scan():
    """Scheduled task to scan market data"""
    with app.app_context():
        try:
            angel_service = AngelOneService()
            if angel_service.login():
                data = angel_service.scan_top_gainers(limit=50)
                print(f"Scheduled scan completed: {len(data)} stocks updated")
        except Exception as e:
            print(f"Scheduled scan error: {e}")

scheduler = BackgroundScheduler()
# Run every 5 minutes during market hours (9:15 AM - 3:30 PM IST)
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
        "message": "Nifty50 Top Gainers Scanner API",
        "version": "1.0.0",
        "endpoints": {
            "top_gainers": "/api/top-gainers",
            "top_losers": "/api/top-losers",
            "all_stocks": "/api/all-stocks",
            "market_summary": "/api/market-summary",
            "refresh": "/api/refresh"
        }
    })

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
