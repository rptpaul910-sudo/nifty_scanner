import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Angel One API Credentials
    ANGEL_API_KEY = os.getenv('ANGEL_API_KEY')
    ANGEL_CLIENT_ID = os.getenv('ANGEL_CLIENT_ID')
    ANGEL_PASSWORD = os.getenv('ANGEL_PASSWORD')
    ANGEL_TOTP_SECRET = os.getenv('ANGEL_TOTP_SECRET')
    
    # MySQL Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'nifty50_scanner')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
