import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL Configuration
    MYSQL_HOST     = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER     = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB       = os.getenv('MYSQL_DB', 'nifty50_scanner')

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG      = os.getenv('DEBUG', 'True').lower() == 'true'
