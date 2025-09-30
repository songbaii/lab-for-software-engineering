create DATABASE if NOT EXISTS soft_ware_engineering;
use soft_ware_engineering;
drop table if EXISTS user;
CREATE table if NOT EXISTS user(
    user_name VARCHAR(50),
    user_id int,
    pass_word VARCHAR(50) NOT NULL,
    PRIMARY KEY(user_name, user_id)
);

drop TABLE if EXISTS user_judge;
CREATE TABLE if NOT exists user_judge(
    user_name VARCHAR(50),
    user_id int,
    movie_id int,
    comment int,# 这里限制一下比如说1-10
    Foreign Key (user_name) REFERENCES user(user_name),
    Foreign Key (user_id) REFERENCES user(user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    PRIMARY KEY(user_name, user_id, movie_id),
    check (comment>=1 and comment<=10)
);
#至此用户部分完成
drop Table if EXISTS movie;
CREATE TABLE if NOT EXISTS movie(
    movie_id int PRIMARY KEY,
    movie_name VARCHAR(50),
    budget int,
    original_language varchar(5),
    popularity int,# 这里为了存储空间，考虑使用int
    release_date date,
    revenue int,# 此处用万元做单位
    vote_count int,# 评分人数
    vote_average int,# 评分的均分
    overview VARCHAR(2000)
);

drop Table if EXISTS movie_genre;
