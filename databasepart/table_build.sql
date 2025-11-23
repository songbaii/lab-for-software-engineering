
drop DATABASE soft_ware_engineering;
create DATABASE if NOT EXISTS soft_ware_engineering;
use soft_ware_engineering;
drop TABLE if EXISTS user_judge;
drop table if EXISTS user;
drop Table if EXISTS movie_genre;
drop TABLE if exists genre_table;
drop table if exists movie;
CREATE table if NOT EXISTS user(
    user_id int primary key auto_increment,
    user_name VARCHAR(50),
    password VARCHAR(50) NOT NULL
); # check

CREATE TABLE if NOT EXISTS movie(
    movie_id int PRIMARY KEY auto_increment,
    movie_name VARCHAR(1000),
    release_year SMALLINT
); # check and done

CREATE TABLE if NOT exists user_judge(
    user_id int,
    movie_id int,
    rating DECIMAL(2,1),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  # 添加时间戳字段
    Foreign Key (user_id) REFERENCES user(user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    PRIMARY KEY(user_id, movie_id),
    check (rating > 0 AND rating <= 5.0 AND (rating * 2) = FLOOR(rating * 2)) # 小数部分只能是0或5, 0.5-5
); # check
#至此用户部分完成

create Table if not exists genre_table(
    genre_id SMALLINT PRIMARY key auto_increment,
    genre_name VARCHAR(20)
);# check and done

create Table if not exists movie_genre(# 影片的类别
    movie_id int,
    genre_id SMALLINT,
    Foreign Key (movie_id) REFERENCES movie(movie_id),
    Foreign Key (genre_id) REFERENCES genre_table(genre_id),
    PRIMARY key(movie_id, genre_id)
); # check and done

create table if not exists user_comment(
    user_id int,
    movie_id int,
    comment VARCHAR(1000),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  # 添加时间戳字段
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    PRIMARY KEY(user_id, movie_id)
); # check and done