import os
import secrets

class Config:
    # MySQL数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'violet')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 's131601')
    MYSQL_DB = os.getenv('MYSQL_DB', 'soft_ware_engineering')

    # SQLAlchemy配置
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'init_command': "SET SESSION sql_mode='NO_ENGINE_SUBSTITUTION'"
        }
    }