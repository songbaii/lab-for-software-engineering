from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime

# 这里使用了 flask_sqlalchemy 库的 SQLAlchemy 类
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }