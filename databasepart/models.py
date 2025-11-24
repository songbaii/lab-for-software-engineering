from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50))
    password = db.Column(db.String(50), nullable=False)

    def check_password(self, password):
        return self.password == password


class Movie(db.Model):
    __tablename__ = 'movie'

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(1000))
    release_year = db.Column(db.SmallInteger)


class UserJudge(db.Model):
    __tablename__ = 'user_judge'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    rating = db.Column(db.DECIMAL(2, 1))  # DECIMAL(2,1) 对应 0.0 到 5.0
    unix_timestamp = db.Column(db.Integer)  # INT UNSIGNED 在 SQLAlchemy 中通常用 Integer

class GenreTable(db.Model):
    __tablename__ = 'genre_table'

    genre_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    genre_name = db.Column(db.String(20))


class MovieGenre(db.Model):
    __tablename__ = 'movie_genre'

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    genre_id = db.Column(db.SmallInteger, db.ForeignKey('genre_table.genre_id'), primary_key=True)


class UserComment(db.Model):
    __tablename__ = 'user_comment'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    comment = db.Column(db.String(1000))
    unix_timestamp = db.Column(db.Integer)  # INT UNSIGNED 在 SQLAlchemy 中通常用 Integer