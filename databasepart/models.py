from flask_sqlalchemy import SQLAlchemy

# 这里使用了 flask_sqlalchemy 库的 SQLAlchemy 类
db = SQLAlchemy()


class User(db.Model):
    __table__ = db.Table(
        'user',
        db.metadata,
        autoload_with=db.engine  # 自动从数据库加载表结构
    )

    def check_password(self, password):
        if self.password != password:
            return False
        else:
            return True

class Movie(db.Model):
    __table__ = db.Table(
        'movie',
        db.metadata,
        autoload_with=db.engine
    )

class UserJudge(db.Model):
    __table__ = db.Table(
        'user_judge',
        db.metadata,
        autoload_with=db.engine
    )

class GenreTable(db.Model):
    __table__ = db.Table(
        'genre',
        db.metadata,
        autoload_with=db.engine
    )

class MovieGenre(db.Model):
    __table__ = db.Table(
        'movie_genre',
        db.metadata,
        autoload_with=db.engine
    )

class UserComment(db.Model):
    __table__ = db.Table(
        'user_comment',
        db.metadata,
        autoload_with=db.engine
    )