from flask_sqlalchemy import SQLAlchemy

# 这里使用了 flask_sqlalchemy 库的 SQLAlchemy 类
db = SQLAlchemy()


class user(db.Model):
    __table__ = db.Table(
        'user',
        db.metadata,
        autoload_with=db.engine  # 自动从数据库加载表结构
    )

class movie(db.Model):
    __table__ = db.Table(
        'movie',
        db.metadata,
        autoload_with=db.engine
    )

class user_judge(db.Model):
    __table__ = db.Table(
        'user_judge',
        db.metadata,
        autoload_with=db.engine
    )

class genre_table(db.Model):
    __table__ = db.Table(
        'genre',
        db.metadata,
        autoload_with=db.engine
    )

class movie_genre(db.Model):
    __table__ = db.Table(
        'movie_genre',
        db.metadata,
        autoload_with=db.engine
    )

class user_comment(db.Model):
    __table__ = db.Table(
        'user_comment',
        db.metadata,
        autoload_with=db.engine
    )