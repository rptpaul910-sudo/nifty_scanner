from flask_mysqldb import MySQL

mysql = MySQL()

def init_db(app):
    """Initialize MySQL connection"""
    mysql.init_app(app)
    return mysql

def save_stock_data(cursor, stock_data):
    """Save stock data to database"""
    query = """
        INSERT INTO stock_prices 
        (symbol, name, token, ltp, open_price, high, low, close_price, 
         change_value, change_percent, volume, recorded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    cursor.execute(query, (
        stock_data['symbol'],
        stock_data['name'],
        stock_data['token'],
        stock_data['ltp'],
        stock_data['open'],
        stock_data['high'],
        stock_data['low'],
        stock_data['close'],
        stock_data['change'],
        stock_data['change_percent'],
        stock_data['volume']
    ))

def get_historical_gainers(cursor, limit=10, days=7):
    """Get historical top gainers"""
    query = """
        SELECT symbol, name, 
               AVG(change_percent) as avg_gain,
               COUNT(*) as appearance_count
        FROM stock_prices
        WHERE recorded_at >= DATE_SUB(NOW(), INTERVAL %s DAY)
          AND change_percent > 0
        GROUP BY symbol, name
        ORDER BY avg_gain DESC
        LIMIT %s
    """
    cursor.execute(query, (days, limit))
    return cursor.fetchall()
