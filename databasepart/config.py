import os
import secrets
from dotenv import load_dotenv
load_dotenv()

class Config:
    # MySQL数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')

    # SQLAlchemy配置
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'init_command': "SET SESSION sql_mode='NO_ENGINE_SUBSTITUTION'"
        }
    }

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER', 'your_username'),
    'password': os.getenv('MYSQL_PASSWORD', 'your_password'),
    'database': os.getenv('MYSQL_DB', 'your_db_name'),
    'charset': 'utf8mb4',
    'autocommit': True,
}